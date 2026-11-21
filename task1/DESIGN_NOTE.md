# task1: which band each paid channel of Zancada's 2027 media plan sits in

## Draw

Subdomain: Cohort and LTV modeling: retention curves, customer lifetime value (Product Analytics, retention-cohort-lifetime-value-modeling)
Analysis type: Forecasting & Predictive Modeling
Answer shape: a forecast path with bands and drivers: each paid channel's 2027 return per euro at the plan's weekly spend and at its stretch spend, each with the range reasonable rebuilds span, and the drivers under it (what the installs a channel bought went on to pay, the installs a week the plan's spend buys, what those installs are worth and what one more euro returns); the growth policy's scale, hold or cut call sits on top
Weight: a hard-to-measure quantity: the twelve-month return of a euro of 2027 spend, which no record holds and three parts of which are each estimated from a different pair of records; of the last five builds on file only task4 sits there (a fleet's losses), and the last three (task5, task8, task9) put their weight elsewhere (`guard.py check task1`, overuse.weight, a WARN)
People: Bernardo Pombo (head of financial planning, who signs the 2027 insertion orders), Magdalena Requena (head of growth, owner of the growth policy), Ester Rey (growth analyst, whose workbook the golden is), Rafa Naranjo (paid acquisition manager, who keeps the budget sheet) (`guard.py names --geo spain --seed 61113`). None appears in the prompt.
Data-native sentence: a store charge reaches Zancada's billing records only when the subscriber next opens the app, the attribution export names an iOS network only for the installs whose users allowed tracking while each network's other installs sit unnamed in one pool and are worth a different fraction of its named ones, and a week's ad spend is what the platform delivered of that week's budget in that week's auction, so the twelve-month return of a euro of 2027 spend has to be estimated from the stores' reports, the networks' install postbacks, the accounts with no channel market by market and week by week, and the weeks the team moved a budget, each read for the part it sees.

Architecture 7, core redrawn in place on 2026-11-21 under the client's phase 2 bar (the guidelines of 11/20 and the closed page as read on 2026-11-21), before any upload: the READY cut of 2026-11-16 (commit 2af8cff) never went to the platform. The phase 2 audit read that cut as fix before testing: two of its three stumps owned no critical component and two components fell with two or three stumps; its second step's remedy was one ratio from a control total, which is the completeness card's fix, under a lesson key the page closed; and its first step sat next to the same card, with the web checkout's subscribers handing its one rate over as checked cases. What moved, all of it proved in `generator/core.py` before any file was touched: (1) the second step's world: an ad network finds its buyers with the signal it gets back from the people it reached, so an install that declined the tracking prompt is the same in its first two days and a weaker subscriber after them, by an amount that differs from network to network; every paid channel but Apple Search Ads runs its campaigns market by market in flights, the postbacks carry the campaign, and the estimate is one ratio per source fitted together across market-weeks; architecture 6's single ratio, the one fully named iOS channel's ratio and an Android look-alike's are now priced shortcuts; (2) the first step's world separates three continuations (a store subscription nobody opens, a subscriber the app still sees, the web checkout's silent subscribers), so no rate read off the records gives the stores' excess; (3) Android's installs that declined tracking are named with their channel, which makes Android the second step's referee; (4) each step owns one critical component, asked for in the decision's words (what the installs each channel bought in the year to 2 November 2025 went on to pay, and the installs a week the plan's spend buys), and the prompt carries four asks. The organisation, its people, the growth policy and the three axes are kept.

The guard's verdict on the registered card (`guard.py check task1`, 2026-11-21) is WARN only, and each warning is answered here: template.chain_near and overuse.weight by the Weight line above and the Template check; overuse.forum (an executive team decides in eleven builds on file) because a media plan of this size is committed by the head of financial planning against a policy the head of growth owns, and the prompt names no one; repeat.deliverables (a CSV and a workbook, as task5, task8 and task9) because that is the house set, and what each holds differs: the workbook's first sheet carries seven bands against two lines with a chart of the returns, the CSV one row per channel; repeat.question_form (which, as task8's prompt) because the decision places each channel in one of three bands, and a placement asks which; skeleton.house_lesson (record_algorithm_inversion is on task22 v2 and task16 v4) because it is one of three lessons here and the call turns on the one no build on file teaches (the Frontier check's Noun swap line).

## Stump screen

Ten candidate traps were put through the seventeen tests of `stumping/references/stump-screen.md` before the card was redrawn; each fix was read against the closed page's "the fix already used" lines.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A. a store charge reaches the billing records only at the subscriber's next open, and the charges never taken in belong to subscriptions nobody opens, which run on a continuation of their own | the stores' excess over the records is spread like the recorded charges (N21, L44) | the stores' monthly reports against the charge dates of the subscriptions last seen set to renew; the web checkout's subscribers, whose every charge is on file | none | kept (S1) |
| B. on iOS an install's channel is on file only with tracking consent; each network's other installs sit unnamed among the accounts with no channel and are worth a network-specific fraction of its named ones | the named installs, or the one fully named channel's ratio, stand for every network (L53, N27, L58) | what the accounts with no channel paid, market by market and week by week, against each network's postbacks less its named installs; Android, where every declined install is named | none | kept (S2) |
| C. a week's spend is what the platform delivered of the week's budget in that week's auction | the response of installs to spend is what more spend buys (L51, L37, L28) | the budget sheet's moved weeks, each move left out of the fit | none | kept (S3) |
| D. one ratio for every source, fitted so that the accounts with no channel add up (architecture 6's second step) | the unnamed installs are worth one common fraction of the named ones | the same pool, read as one total | test 1 (its whole remedy is one factor from a control total, the completeness card's fix) and test 12 (the fully named channel's ratio lands near it) | dropped: priced as a shortcut (Meta iOS 1.38, scale; 45 on the rubric) |
| E. architecture 6's first step as it was graded (one continuation for every silent subscription, the share of revenue the records never took in as its component) | the stores' excess is spread like the recorded charges | the web checkout's subscribers | test 12 (the web checkout's continuation read off the records gave the same figure, an easier second route, and a factor from checked cases is a closed card's fix) and test 14 (its component named the correction) | dropped: the world now separates three continuations and the figure asked for is what an install went on to pay |
| F. a consent gate on Android's attribution as well | the named installs stand for the channel | none: the Play install referrer names every Android install | test 8 (the process does not put it there) and test 11 (no record would let the estimate be checked) | dropped: Android is the second step's referee instead |
| G. the stores' commission tier by a developer's yearly proceeds | one commission for every charge | the stores' proceeds columns | tests 3 and 4 (a filed rate, executed) | dropped: the policy files 15 per cent |
| H. a channel's installs partly taken from organic, and its audience used up at a higher spend | every bought install is additional | none in a pack of this kind | test 1 (the incrementality and the used-up easy cases cards) | dropped |
| I. the youngest install weeks completed to twelve months by a curve | young cohorts follow the old ones | the mature weeks' own curves | test 1 (the young cohorts card) and test 2 (a reflex) | dropped: the twelve months are read only on the weeks that have them |
| J. a response curve of installs on weekly spend with a month pattern | the curve's shape | held-out weeks | test 2 (the field's textbook curve, fitted on sight) and test 15 | dropped: it is S3's hurried route |

## Deep reasoning

Task type: retention cohort lifetime value modeling (Cohort and LTV modeling: retention curves, customer lifetime value), which serves Forecasting
Domain test: every result is an acquisition-economics and lifetime-value quantity of a subscription app: what an install went on to pay in its first twelve months where the app's records stop at the last open, what a network's installs are worth where the attribution export names no channel, the installs a weekly budget buys in an ad auction, the value of those installs, the return per euro at a plan's spend and what the next euro returns; it is the growth analyst's own lifetime-value and payback work.
Swap: "hold AppLovin because the stores go on charging the subscribers who stopped opening the app, hold Meta iOS because its installs the export cannot name are worth under half the ones it can, hold Google Android because its cheap weeks were the auction's doing and not the budget's" makes no sense for a hospital or a grid: there is no store report beside an app's own billing sync, no tracking prompt, no install postback, no campaign flight and no ad auction.
Where the weight sits: the twelve-month net revenue per install of every install each channel bought (R1 and R2): the stores' reports are set against the billing records month by month and the excess put on the subscriptions that were set to take it (a share of the trials last seen unconverted and a monthly continuation, both fitted to the excess), then each iOS network's installs the export does not name are counted from the postbacks by market, week and first-48-hour value, and one ratio per source is fitted so that, market-week by market-week, they add up to what the accounts with no channel paid; R3 to R6 carry that value through what a budget buys.
Layer 1: the attribution partner re-sends rows after an SDK retry and reports second devices as reinstalls; staff and test accounts carry sandbox charges; Apple reports its days in Pacific time and Google in UTC; a postback arrives three or four days after its install and carries no account; the networks' own install counts credit view-throughs; refunds sit in both the stores' reports and the records; the budget sheet rounds to ten euros and the platforms bill to the cent; a paused campaign still bills a few euros of trailing delivery. None decides a band.
Not one thing: three decisive steps on three axes each open their own channel (## Stump factorial, ## Open members): the charges the records never took in (AppLovin Android), the installs the export cannot name (Meta iOS), what a budget buys (Google Android); a run that makes any two of the three still files one channel in the wrong band and earns 44 to 47 on the rubric, a run that makes one earns 25 to 28, and each step owns a critical component the other two do not touch.
One-fact test: the most useful sentence a reviewer could give is the consent one ("each network's installs that declined the tracking prompt are worth a different fraction of its named ones, and they sit unnamed among the accounts with no channel"): on the reflex route it takes the rubric from 16 to 28 and rescues no result whole (0 of 7), and the declined installs by market, week and cell, the organic remainder, one ratio per source fitted together and the thin cells are still to build; the stores' sentence rescues R1 alone and the budget sentence R3 alone (1 of 7 results each, nine rubric points each), and no sentence names two of the three.
Not semantics: every field read as its system writes it still leaves each hurried result wrong: recorded_at says when the app took a charge in and last_open_at when the account last opened, and nothing says which charges are missing or whose they are; the tracking answer is a field on every account and the campaign a field on every postback, and nothing says what a declined install is worth or that it differs by network; the budget sheet and the spend export are two columns of euros, and nothing says which one the team controls in 2027.
Not rule application: the growth policy files the measure, the 365 days, the VAT, the commission and the fee, the marginal return and the lines; no filed procedure reconciles the stores' reports with the records, prices an install the export does not name or says what a budget buys.
Estimand: growth policy sections 2.1 to 2.6 (the return, an install, the twelve months, net revenue, prices and the trial, the marginal return), section 1 (the channels the policy places) and section 3 (the lines); the media plan's 52 weekly spends and its stretch spends; the prompt's populations (the installs each channel's 2027 plan spend buys; the installs each channel bought in the year to 2 November 2025), outcome (their twelve-month net revenue), window (the 365 days from each install) and units (euros per euro of spend; installs a week; euros per install; euros per extra euro).
No decoy: no document argues a band; the networks' own install counts and the export's named installs are what those systems record, and no file carries a return or a value per install per channel.
No replay: no result re-derives a published figure and no stated number is wrong.
Pinned: every graded figure is banded by the 32 variants of `generator/core.py` (## Pinning list, Variant battery) and the call holds under every one; the rivals outside the bands are the hurried choices and the stronger shortcuts of each step, each refuted by a figure from the shipped files (the web checkout's charges after the last open and the share of the stores' renewal excess each continuation takes in; what the accounts with no channel paid, the test of equal ratios and Android's named declined installs; the moved weeks), and the file-level conventions are closed in the fork table and asserted on the cut pack.
Run forecast: R1 lost to a method shortcut (the stores' excess spread over the recorded charges month by month, N21, L44); R2 to a method shortcut (every postback priced at the named installs' value or at the one labelled channel's ratio, L53, N27, L58); R3 and R6 to a self-confirming check (the response fitted on spend wins its own hold-out against the budget, L51, L37, L28); R4, R5 and R7 to dismissed own evidence on all three.
Strategy label: UNTESTED (a pool with no source labels apportioned by one fitted ratio per source, with record_algorithm_inversion and endogenous_supply_instrument)
Depth level: 5 by `generator/core.py` (CORE PASS level 5): three decisive steps on three axes, each necessary alone and none sufficient, three open channels each opened by its own step, each step with a critical component of its own, seven distinct wrong calls across the lattice and three among the single drops.
Lesson: a channel's twelve-month return is a quantity no record holds, and each part of it is estimated from the record that sees it and ruled on where it is known: the stores' reports for the charges the app never took in (put on the subscriptions set to take them at their own continuation, not spread over the recorded ones), the pool of accounts with no channel for the installs the export cannot name (one ratio per network fitted from how the pool's revenue moves as each network's share of it moves across markets and weeks, not one ratio borrowed from a labelled source), and the team's own budget moves for what a budget buys (the week's spend being the auction's outcome); no build on file teaches the second, and none the three together.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | what an install bought on each Android channel in the year to 2 November 2025 went on to pay in its first twelve months, net (AppLovin Android EUR 4.87, Google Android EUR 8.60) | missingness and measurement | policy 2.2 to 2.4 (every charge made in the 365 days, net); the stores' daily reports, the records' charges, each account's last open, plan and renewal setting as last seen | AppLovin Android 4.83 to 4.91; Google Android 8.56 to 8.62 | method shortcut: each recorded charge scaled by its store-month's ratio of charged to recorded, which reconciles to the stores' reports in every month and files 3.70 and 7.88 | independent: the stores' reports, the billing records and the accounts' last opens | Component 1, Ask 4 |
| R2 | the same for each iOS network, over every install it bought (Meta iOS EUR 5.78, TikTok iOS 4.98, Snapchat iOS 6.10, Google iOS 9.47, Pinterest iOS 9.37) | decomposition and attribution | policy 2.2 (each install bought by at most one channel, whether or not the partner can name it); the install postbacks by campaign and first-48-hour value, the named installs, the accounts with no channel and what they paid, market by market and week by week | Meta iOS 5.67 to 6.00; each network's own range from the battery | method shortcut: every postback priced at the value the network's named installs showed at the same first-48-hour value (Meta iOS 9.55), or that value times the ratio the one fully named iOS channel shows (8.59) | R1 | Component 2, Ask 4 |
| R3 | the installs a week the plan's weekly spend buys on each channel (Google Android 611; Meta iOS 789, TikTok iOS 750, Snapchat iOS 643, Google iOS 624, Pinterest iOS 325, AppLovin Android 932) | causal reasoning | the media plan's 52 weekly spends; the budget sheet, the platforms' daily spend and each channel's installs by week | Google Android 596 to 627; each channel's own range from the battery | self-confirming check: installs fitted on the week's spend, which beats the budget alone on held-out weeks (10 against 21 per cent mean error) because the auction that moves spend moves installs with it; it files 511 on Google Android | independent: the budget sheet, the daily spend and the weekly installs | Component 3, Ask 2 |
| R4 | the twelve-month net revenue per install of the installs the plan's spend buys (Meta iOS EUR 5.64, TikTok iOS 4.80, Snapchat iOS 5.93, Google iOS 9.36, Pinterest iOS 10.20, Google Android 9.34, AppLovin Android 4.95) | forecasting | policy 2.1 and 2.3; R1 and R2 carried through the value's response to the budget over R3's weeks | per channel (Meta iOS 5.53 to 5.85, AppLovin Android 4.90 to 4.99) | dismissed own evidence: the true-up, the named installs' value and the response on spend together file Meta iOS 9.52 and AppLovin Android 3.73 | R1, R2, R3 | Ask 2 |
| R5 | each channel's 2027 return per euro at the plan's weekly spend and at its stretch spend (plan: Pinterest iOS 1.58, Google iOS 1.45, Meta iOS 1.05, Google Android 1.04, AppLovin Android 0.97, Snapchat iOS 0.62, TikTok iOS 0.55; stretch: 1.18, 1.25, 0.93, 0.94, 0.85, 0.58, 0.52) | forecasting | policy 2.1; the media plan's plan and stretch spends; R3 and R4 | per channel (plan: Meta iOS 1.03 to 1.09, Google Android 1.02 to 1.06, AppLovin Android 0.94 to 1.00) | dismissed own evidence: the three shortcuts together file Meta iOS 1.84, Google Android 0.78 and AppLovin Android 0.71 at the plan's spend | R3, R4 | Ask 1 |
| R6 | what one more euro on top of the plan's weekly spend returns (Meta iOS 0.56, TikTok iOS 0.33, Snapchat iOS 0.34, Google iOS 0.73, Pinterest iOS 0.75, Google Android 0.58, AppLovin Android 0.62) | modeling | policy 2.6; the two fitted responses (installs and value per install to the budget) at the plan's spend | per channel (Google Android 0.55 to 0.59, Meta iOS 0.52 to 0.58) | self-confirming check: the two slopes read on spend, where installs rise in proportion to spend, which files 0.63 to 1.54 | R3, R4 | Ask 3 |
| R7 | each channel's band: scale Google iOS and Pinterest iOS; hold Meta iOS, Google Android and AppLovin Android; cut TikTok iOS and Snapchat iOS | synthesis | policy section 3 (cut under 0.90, hold from 0.90, scale from 1.20) | exact | dismissed own evidence: scales Meta iOS and cuts Google Android and AppLovin Android | R5 | Recommendation |

Carry-forward: the blocks state 42 figures (three components and 39 ask figures), six figures for each of seven channels. Each stump owns one of them, its critical component, which falls with that stump alone: AppLovin Android's twelve-month net revenue per install with S1 (EUR 4.87, 3.70 when S1 is lost), Meta iOS's with S2 (5.78, 9.55 when lost) and Google Android's installs a week at the plan's spend with S3 (611, 511 when lost). Of the 42, 7 fall with all three stumps (TikTok's and Snapchat's two returns and their next euro, Google iOS's stretch return), 16 with two, 16 with one and 3 with none (the installs a week on Snapchat iOS, Google iOS and AppLovin Android, where the response on spend lands inside the range the delivery-share variants set); S1 moves 24 figures outside their bands, S2 23 and S3 22, so a run that loses any one step earns 44 to 47. R1 is upstream of five of the other six results because the twelve-month value of every install runs through the charges the records never took in; none of the five hangs on it alone (R2 needs S2, R4 to R7 need S2 and S3 as well, and R3 does not depend on it). Reflex work (the installs each channel bought, the recorded charges, the weekly spend, the unattributed accounts' count) is done on every route and stated only in the Step-by-Step.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a subscriber who stops opening the app keeps paying, the app takes a store charge into its records only at the next open, and a store subscription nobody opens is rarely cancelled | constructed, the process of client-side receipt sync and forgotten subscriptions | no: every channel, both stores and organic, from 10 per cent of Google iOS's twelve-month revenue to 36 per cent of AppLovin Android's | modelling: the stores' excess month by month against the charge dates of the subscriptions last seen set to renew | modelling (a share of trial-end candidates charged and a monthly continuation fitted to the excess, carried account by account) | keep |
| an install that declined the tracking prompt sent its network no signal back, so it is the same in its first two days and a weaker subscriber after them, by an amount that differs by network | constructed, the documented behaviour of the tracking prompt and of signal-based ad delivery | no: every paid channel on both platforms, every market and every week (a declined install is worth 0.45 of a named one on Meta iOS and 0.86 on Google iOS, 0.63 and 0.77 on the two Android channels, 0.89 on Apple Search Ads; 73 per cent of iOS installs and 46 per cent of Android installs declined) | modelling: each source's declined installs by market, week and first-48-hour value set against what the accounts with no channel paid | modelling (one ratio per source fitted together across 156 market-weeks) | keep |
| a platform spends more of a weekly budget in the weeks its auction is cheap, and those weeks bring more installs | constructed, the delivery of a budgeted campaign in an auction | no: all eight channels in all 104 weeks | modelling: installs against the budget with the delivery beside it, checked on the weeks the team moved a budget | modelling (a response to the budget carried to the budget that delivers the plan's spend) | keep |
| the team buys each network market by market in flights | constructed, how a small team runs three markets | no: every paid channel but Apple Search Ads, in all three markets (a channel is live in 37 to 85 per cent of a market's weeks) | a targeted query: the campaigns' live weeks by market | nothing to correct: it is what lets the second factor's ratios be told apart, a judgment about which variation to fit on | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 what an install on each Android channel went on to pay in twelve months | Missed | Missed | Right |
| R2 what an install on each iOS network went on to pay in twelve months | Missed | Missed | Right |
| R3 the installs a week the plan's spend buys | Missed | Partly | Right |
| R4 the twelve-month net revenue per install of the installs the plan's spend buys | Missed | Missed | Right |
| R5 each channel's return per euro at the plan's and at the stretch spend | Missed | Missed | Right |
| R6 what one more euro on top of the plan's weekly spend returns | Missed | Missed | Right |
| R7 each channel's band | Missed | Missed | Right |
| Roughly | 0 of 7 | 0.5 of 7 | 7 of 7 |

Measured by: generator/core.py on .claude/skills/stumping/corelib.py at the draw (the rubric table of ## Stump core: the quick pass is the direct route, which lands one figure of the 42; the careful but hurried pass is the reflex route, which lands five, three of them R3's); .claude/skills/stumping/effort.py on generator/effort.json once the pack is cut
Largest single hint: any one of the three sentences rescues 1 of 7 results at most: the consent sentence (each network's installs that declined the tracking prompt are worth a different fraction of its named ones, and they sit unnamed among the accounts with no channel) adds the most rubric points, twelve (16 to 28), and rescues no result whole; the stores' sentence rescues R1 and the budget sentence R3, nine points each
Pair estimate: 16 (the reflex route on corelib's rubric: instruction-following and five figures, the call wrong on three channels; the rigorous standard route earns 20, and a run that loses one step alone 44, 45 or 47)

## Stump core

From `python3 task1/generator/core.py` (SEED 71126 for the people, BUDGET_SEED 71116 for the budgets and the auctions, CAL_SEED 7360 for the campaign flights; 748,034 accounts; 32 variants), every figure as printed. The draw was chosen, and the choice is on the record: the campaign calendar was kept among seven compared by how precisely each identifies the five networks' ratios over six draws of the people (root mean square error 0.013 to 0.031 by source on the one kept, up to 0.049 on the others), and the people's seed among 29 scanned draws as one where the fit sits near the world's own figures on all three steps and the battery's spread is narrow. On five other draws of the people (seeds 72126 to 76126, chosen on nothing) the golden files the world's call for all seven channels every time, and a step lost alone moves its own channel across its line on all five for S1 and S2 and on four of five for S3 (on seed 73126, where Google Android's golden return is 1.115, the response on spend leaves it in hold).

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| AppLovin Android | 0.9/1.2 | 0.9702 | 0.0215 | 0.7078 | 0.5813 | 0.7078 | S1 |
| Google Android | 0.9/1.2 | 1.04 | 0.0142 | 0.7815 | 0.6242 | 0.7815 | S3 |
| Google iOS | 0.9/1.2 | 1.45 | 0.0456 | 1.751 | 0.4348 | 1.542 | forced |
| Meta iOS | 0.9/1.2 | 1.05 | 0.0279 | 1.842 | 0.4872 | 1.622 | S2 |
| Pinterest iOS | 0.9/1.2 | 1.578 | 0.0716 | 1.684 | 0.408 | 1.484 | forced |
| Snapchat iOS | 0.9/1.2 | 0.6207 | 0.0125 | 0.7986 | 0.2095 | 0.7013 | forced |
| TikTok iOS | 0.9/1.2 | 0.5489 | 0.0132 | 0.7601 | 0.1886 | 0.6685 | forced |

| Figure | Block | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|
| return Meta iOS | asks | 1.05 | 1.029 to 1.088 | - | flips | - | lost |
| return TikTok iOS | asks | 0.5489 | 0.5361 to 0.5673 | moves | moves | moves | lost |
| return Snapchat iOS | asks | 0.6207 | 0.6028 to 0.6394 | moves | moves | moves | lost |
| return Google iOS | asks | 1.45 | 1.387 to 1.493 | moves | moves | - | lost |
| return Pinterest iOS | asks | 1.578 | 1.499 to 1.68 | - | moves | moves | earned |
| return Google Android | asks | 1.04 | 1.02 to 1.061 | moves | - | flips | lost |
| return AppLovin Android | asks | 0.9702 | 0.9403 to 1.002 | flips | - | - | lost |
| stretch return Meta iOS | asks | 0.9283 | 0.9098 to 0.9606 | - | moves | moves | lost |
| stretch return TikTok iOS | asks | 0.5187 | 0.5066 to 0.5361 | moves | moves | moves | lost |
| stretch return Snapchat iOS | asks | 0.583 | 0.5661 to 0.6005 | moves | moves | moves | lost |
| stretch return Google iOS | asks | 1.25 | 1.195 to 1.286 | moves | moves | moves | lost |
| stretch return Pinterest iOS | asks | 1.175 | 1.154 to 1.244 | - | moves | - | lost |
| stretch return Google Android | asks | 0.9414 | 0.9231 to 0.9605 | moves | - | moves | lost |
| stretch return AppLovin Android | asks | 0.8473 | 0.8212 to 0.8751 | moves | - | moves | lost |
| installs a week Meta iOS | asks | 788.8 | 778.8 to 799.2 | - | - | moves | lost |
| installs a week TikTok iOS | asks | 750.2 | 729.7 to 769.8 | - | - | moves | lost |
| installs a week Snapchat iOS | asks | 642.6 | 617.1 to 669.2 | - | - | - | earned |
| installs a week Google iOS | asks | 624.2 | 608 to 639.5 | - | - | - | earned |
| installs a week Pinterest iOS | asks | 325 | 312 to 329.8 | - | - | moves | lost |
| installs a week Google Android | components | 610.8 | 595.6 to 626.8 | - | - | moves | lost |
| installs a week AppLovin Android | asks | 931.6 | 895.4 to 970.2 | - | - | - | earned |
| value at plan Meta iOS | asks | 5.639 | 5.525 to 5.849 | - | moves | - | lost |
| value at plan TikTok iOS | asks | 4.795 | 4.702 to 4.951 | moves | moves | - | lost |
| value at plan Snapchat iOS | asks | 5.926 | 5.845 to 6.049 | moves | moves | - | lost |
| value at plan Google iOS | asks | 9.362 | 8.957 to 9.625 | moves | moves | - | lost |
| value at plan Pinterest iOS | asks | 10.2 | 9.908 to 10.82 | - | moves | - | lost |
| value at plan Google Android | asks | 9.34 | 9.25 to 9.511 | moves | - | moves | lost |
| value at plan AppLovin Android | asks | 4.946 | 4.901 to 4.986 | moves | - | - | lost |
| next euro Meta iOS | asks | 0.5562 | 0.5243 to 0.5847 | - | moves | moves | lost |
| next euro TikTok iOS | asks | 0.327 | 0.317 to 0.3496 | moves | moves | moves | lost |
| next euro Snapchat iOS | asks | 0.3421 | 0.3224 to 0.3627 | moves | moves | moves | lost |
| next euro Google iOS | asks | 0.7299 | 0.5874 to 0.7819 | - | - | moves | lost |
| next euro Pinterest iOS | asks | 0.7462 | 0.7002 to 0.8666 | - | - | moves | lost |
| next euro Google Android | asks | 0.5766 | 0.5492 to 0.5916 | moves | - | moves | lost |
| next euro AppLovin Android | asks | 0.6166 | 0.5783 to 0.6756 | moves | - | moves | earned |
| paid per install Meta iOS | components | 5.783 | 5.665 to 5.996 | - | moves | - | lost |
| paid per install TikTok iOS | asks | 4.976 | 4.88 to 5.139 | moves | moves | - | lost |
| paid per install Snapchat iOS | asks | 6.104 | 6.021 to 6.23 | moves | moves | - | lost |
| paid per install Google iOS | asks | 9.466 | 9.055 to 9.738 | moves | moves | - | lost |
| paid per install Pinterest iOS | asks | 9.368 | 9.196 to 9.914 | - | moves | - | lost |
| paid per install Google Android | asks | 8.604 | 8.557 to 8.619 | moves | - | - | lost |
| paid per install AppLovin Android | components | 4.874 | 4.832 to 4.908 | moves | - | - | lost |

| Route | Call | Earns on the rubric |
|---|---|---|
| golden | right | 100 |
| S1 lost alone | wrong | 44 |
| S2 lost alone | wrong | 45 |
| S3 lost alone | wrong | 47 |
| S1 fixed alone | wrong | 25 |
| S2 fixed alone | wrong | 28 |
| S3 fixed alone | wrong | 25 |
| reflex route (every stump lost) | wrong | 16 |
| rigorous standard route | wrong | 20 |

CORE PASS level 5

Unobserved part: the twelve-month net revenue a euro of each channel's 2027 plan spend returns. No record holds three parts of it: the store charges made after a subscriber's last open (the records hold 374,342 of the 537,959 monthly charges the stores made, and what is missing runs from a tenth of Google iOS's twelve-month revenue to 36 per cent of AppLovin Android's), the channel of an iOS install whose user declined tracking (73 per cent of each network's installs, 273,830 accounts with no channel) and with it what those installs went on to pay, and the installs a budget would have bought in a week whose auction had been different (a week's spend moves with the auction as well as with the budget).
Instruments: the billing records see every charge up to each account's last open and every web-checkout charge; read raw with the installs the export names and the last full year's return (the direct route) they file returns of 0.19 to 0.62 and every channel in cut. The stores' daily reports see every store charge by product, event and storefront, with no account. The attribution export sees the channel of every Android install and every Apple Search Ads install, and of an iOS network's install only where the user allowed tracking (27 per cent). The install postbacks see every install of the five iOS networks with its campaign (so its market), arrival day and first-48-hour value, with no account. The accounts with no channel hold each network's declined installs and the organic declined ones together, 138,896 accounts in the mature year. The tracking answer is on every account. The budget sheet sees the weekly budget the team set on each channel and its 72 moves; the platforms' spend export sees what was delivered.
Referee: three slices the plan's channels at their 2027 spend do not reach. S1: the web checkout's AppLovin Android subscribers (240 with a charge on file before the last open), whose every charge the backend holds: the net revenue charged after the last open inside the twelve months is 31.79 per subscriber, the first step's fit run on the web checkout's own months files 31.82 and the proportional true-up 13.59 (the stores' fitted continuation carried over without refitting would file 50.91: the fitted continuation is 0.878 on the web checkout and 0.972 on a store, which is why the fit is run where the subscriptions are). S2: AppLovin Android's 22,869 installs that declined the prompt, their channel set aside as it is on iOS: they paid 3.29 per install, the second step's fit run on Android files 3.55, their named installs' value by first-48-hour value 5.26, Apple Search Ads' ratio 4.50 and one ratio for every source 4.26 (the weakest rival's error is 3.7 times the golden's; this is the slice passed to corelib). S3: Google Android's nine budget moves, each left out of the fit in turn: installs in the raised weeks over installs in the lowered weeks 1.403, the golden's fit 1.434, the fit on spend 1.872 (15 times the golden's error; spend instrumented by the budget 1.415, the budget alone 1.412). Read raw as the answer none files a band: the web checkout is 15 per cent of subscribers, Android has no unnamed install, and the moved weeks are 33 of Google Android's 104.
Strongest standard route: AppLovin Android: the records trued up to the stores' reports month by month (a control total that reconciles exactly) and the response fitted on spend with its hold-out, 0.708 (cut); refuted by the web checkout's subscribers (13.59 against 31.79 after the last open). Meta iOS: every postback priced by first-48-hour value at its named installs' value times the ratio Apple Search Ads' declined installs show (the one labelled check iOS offers), on trued-up records, 1.622 (scale); refuted by the accounts with no channel, which that pricing puts at 1.21 times what they paid, and by AppLovin Android's declined installs (4.50 against 3.29). Google Android: installs and value fitted on weekly spend with a month pattern and held-out weeks, 0.782 (cut); refuted by its own budget moves (1.872 against 1.403). The route earns 20 on the rubric.
Said out loud: S1 "a store charge reaches the app's billing records only when the subscriber next opens the app, so the stores' excess over the records belongs to subscriptions last seen still set to renew, not to every account in proportion": four steps left (the candidates and their next charge dates; the share of trial-end candidates charged, by store and by how trial starters of the same first two days went on to buy; the monthly continuation of a subscription nobody opens, fitted to the stores' renewal excess month by month, which is neither the web checkout's nor the one the app saw; the charges carried account by account inside each install's 365 days). S2 "on iOS the attribution export names an install's channel only where the user allowed tracking; each network's other installs sit unnamed among the accounts with no channel, and how much less they are worth than its named ones differs from network to network": five steps left (each network's declined installs by market, week and first-48-hour value, the postbacks dated back to their install week less the named installs; the organic declined installs as the remainder; each source's named value by cell with the thin cells handled; one ratio per source fitted together across market-weeks; the ratios carried into each network's value per install and into each week's value for the response). S3 "a week's spend is what the platform chose to deliver of the week's budget given that week's auction, so weeks of high and low spend are not weeks of high and low budgets; what a budget buys shows in the weeks the team moved it": three steps left (installs and value per install fitted on the budget with the delivery beside it; the level set to the history; the plan's spend turned into the budget that delivers it).
Worth: S1 0.234 on AppLovin Android, 10.9 times the family's spread of 0.0215. S2 0.684 on Meta iOS, 24.5 times 0.0279. S3 0.188 on Google Android, 13.2 times 0.0142. Each open member's margin to its nearest line (AppLovin Android 0.070, Meta iOS 0.150, Google Android 0.140) is three to ten times its family's spread and smaller than its stump's worth.
Regimes: second stump on every member, each with its own regime. S1's continuation is checked on the web checkout's subscribers (where the same fit gives 0.878 and lands the charges after the last open) and cannot be checked on a store subscriber, where the fit to the stores' excess is the only basis (0.972; carried at the web checkout's 0.878 it takes in 56 per cent of the stores' renewal excess, at the 0.91 the app saw 65 to 68 per cent). S2's ratios are checked on Android, where every declined install is named, and on Apple Search Ads (0.890 labelled); they cannot be checked network by network on iOS and fail when one ratio is carried across networks (0.44 to 0.90). S3's response is checked on each channel's own moved weeks; every plan and stretch budget sits inside the budgets on record (Google Android's plan budget near the low end, Google iOS's stretch near the top). S1 opens AppLovin Android, S2 Meta iOS, S3 Google Android.
Sharp: S1: its wrong route passes the control total (the trued-up records equal the stores' reports in every month); its right route commits to which subscriptions took the unseen charges and at what continuation (0.97 a month on a store, against 0.91 where the app still saw the subscriber and 0.88 on the web checkout); the evidence is in the stores' monthly excess beside the charge dates of the subscriptions last seen set to renew; the correction runs from a tenth of Google iOS's revenue to 36 per cent of AppLovin Android's, where the true-up moves Google iOS up 8 per cent and AppLovin Android down 24; its own figure is AppLovin Android's twelve-month net revenue per install (4.87, 3.70 on the true-up). S2: its wrong route passes two checks (each network's postbacks reconcile to named and unnamed installs cell by cell, and the one labelled iOS channel confirms the correction it applies); its right route commits to a ratio per network where the labelled sources show only 0.63 to 0.89; the evidence is in what the accounts with no channel paid by market and week beside each network's campaign flights; the correction is 0.44 on Meta iOS, 0.52 on TikTok iOS, 0.61 on Snapchat iOS, 0.81 on Pinterest iOS and 0.90 on Google iOS; its own figure is Meta iOS's twelve-month net revenue per install (5.78; 9.55 at the named value, 8.59 at Apple Search Ads' ratio, 7.62 at one ratio for every source, 7.05 at the Android look-alike's). S3: its wrong route passes a hold-out (on every fourth week the fit on spend misses installs by 10.0 per cent and the budget alone by 20.6; on the last quarter 12.5 and 22.3); its right route commits to the budget as what the team sets in 2027 (elasticities of 0.68 to 0.80 against 0.97 to 1.09 on spend); the evidence is in the budget sheet's 72 moves over 286 weeks (each move left out, the fit on spend misses those weeks' installs by 13.1 per cent and the golden's by 3.5); read on spend the return rises 4 to 8 per cent on the four networks whose budgets the plan raises and falls on the three it cuts (Google Android 18 per cent, Pinterest iOS 14, AppLovin Android 4); its own figure is Google Android's installs a week at the plan's spend (611, 511 on spend).
Earns: a run that loses only S1 earns 44, only S2 45, only S3 47 (50 or under each); the reflex route earns 16 and the rigorous standard route 20 (30 and 50 or under); S1 fixed alone earns 25, S2 fixed alone 28, S3 fixed alone 25 (each over the reflex route, a third at most). The reflex route still lands five figures: Pinterest iOS's return (1.684 against a range to 1.680, inside the near-miss allowance), the installs a week on Snapchat iOS, Google iOS and AppLovin Android (the response on spend sits inside the range the two delivery-share variants set) and AppLovin Android's next euro (0.676 against a range to 0.676); each is kept, because an ask is the same figure for every channel and no channel can be left out of it. Every other shortcut priced the same way, the other two steps golden: S1 one true-up factor per store 43, the candidates carried at the cancellations the app saw 42 or at the web checkout's continuation 36, the records as they stand 25; S2 the named installs alone 43, one ratio for every source 45, the pool's own value 47, the Android look-alike's ratio 51, organic pinned at Apple Search Ads' ratio with one ratio for the networks 51, Apple Search Ads' ratio 56, a fit with the four social networks sharing one ratio 58 (each of these wrong on Meta iOS); S3 the two years' average return 39. Four S2 shortcuts therefore sit over the house line of 50 and under the bar of 60, and three finer poolings of the fit (Meta, TikTok and Snapchat sharing one ratio 81; Meta with TikTok 93; TikTok with Snapchat 89) land the call: they are what a run earns for building the second step and pooling where the fit says not to (SF23).

## Stump factorial

Reflex route: the installs of each iOS network counted from its postbacks and of the other channels from the channel on file; re-sent export rows, reinstalls, staff accounts and sandbox charges left out; net revenue at the policy's VAT, commission and fee; the twelve months read on the 52 install weeks that have them; the billing records trued up to the stores' reports month by month; every postback priced at the value its network's named installs showed at the same first-48-hour value; installs and value per install fitted on weekly spend with a month pattern and held-out weeks, carried to the plan's and the stretch spend. It files Meta iOS 1.84 (scale), Google Android 0.78 (cut) and AppLovin Android 0.71 (cut) against three holds, the other four bands right, and earns 16 on the rubric; this route is the careful but hurried pass.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 the stores' excess over the billing records belongs to the subscriptions nobody opens, carried at a continuation of their own fitted to that excess | stump | each recorded charge scaled by its store-month's ratio of charged to recorded | N21, L44 | AppLovin Android cut (0.74) | Meta iOS scale (1.82), Google Android cut (0.85), TikTok iOS and Snapchat iOS hold (0.90 each), four bands still wrong; rescues R1 | no: the candidates, the trial-end share, the continuation fitted to the stores' excess and the carry account by account |
| S2 each network's installs that declined tracking sit unnamed among the accounts with no channel and are worth a network-specific fraction of its named ones | stump | every postback priced at its network's named installs' value by first-48-hour value | L53, N27, L58 | Meta iOS scale (1.73) | Google Android cut (0.78) and AppLovin Android cut (0.71), two bands still wrong; no result rescued whole | no: the declined installs by market, week and cell, the organic remainder, one ratio per source fitted together, the thin cells and the carry into each week's value |
| S3 a week's spend is the auction's outcome, so what a budget buys is read on the budget with the delivery beside it | stump | installs and value fitted on weekly spend, certified on held-out weeks | L51, L37, L28 | Google Android cut (0.85) | Meta iOS scale (1.75) and AppLovin Android cut (0.74), two bands still wrong; rescues R3 | no: the estimator, the level set to the history and the budget that delivers the plan's spend |
| J4 each iOS network's installs counted from its install postbacks and set against its named installs | reflex | - | R81, R93 | same call | - | - |
| J5 re-sent rows, reinstalls, staff and test accounts and sandbox charges left out | reflex | - | growth policy 2.2; R93 | same call | - | - |
| J6 net revenue at the policy's VAT, commission and fee, over the 365 days from the install | reflex | - | growth policy 2.3 and 2.4 | same call | - | - |
| J7 a response curve with a month pattern and held-out weeks fitted to the weekly record | reflex | - | R92 | same call | - | - |

Level: 5: three necessary stumps, none sufficient alone, the single drops on three distinct wrong calls and the seven shortcut routes of the lattice on seven.

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| AppLovin Android | 0.970, hold (0.070 above 0.90) | 0.0215 | 0.708, cut (wrong) | 0.581, cut (wrong) | S1 |
| Meta iOS | 1.050, hold (0.150 under 1.20) | 0.0279 | 1.842, scale (wrong) | 0.487, cut (wrong) | S2 |
| Google Android | 1.040, hold (0.140 above 0.90) | 0.0142 | 0.782, cut (wrong) | 0.624, cut (wrong) | S3 |
| Google iOS | 1.450, scale (0.250 above 1.20) | 0.0456 | 1.751, scale (right) | 0.435, cut (wrong) | forced (the reflex route files its band; four of its six figures fall with two stumps or more) |
| Pinterest iOS | 1.578, scale (0.378 above 1.20) | 0.0716 | 1.684, scale (right) | 0.408, cut (wrong) | forced (as Google iOS) |
| Snapchat iOS | 0.621, cut (0.279 under 0.90) | 0.0125 | 0.799, cut (right) | 0.210, cut (right) | forced |
| TikTok iOS | 0.549, cut (0.351 under 0.90) | 0.0132 | 0.760, cut (right) | 0.189, cut (right) | forced |

Direct route: the pack's most direct evidence read at face value is the billing records as they stand, the installs the export names and the last full year's revenue over its spend (`generator/core.py`, `route(O, "raw", "direct", "average")`): the records miss a tenth to 36 per cent of each channel's revenue and the named installs are about 27 per cent of an iOS network's, so it files every channel under 0.90 (0.19 to 0.62) and puts all three open members and both scale channels in cut. The rigorous standard route (`RIGOROUS`) files AppLovin Android 0.708, Meta iOS 1.622 and Google Android 0.782, each in the wrong band.

## Data provenance

Source: generated by task1/generator from a simulated subscription business: installs bought week by week on eight paid channels and two organic sources under the team's weekly budgets, each week's auction and each channel's campaign flights by market; each person's engagement, reachability and readiness to stop opening an app they pay for; the tracking answer and what a network can learn about an install that declines it; the first two days, the trial, the plan, the store or the web checkout, the monthly charges and the last open; the networks' postbacks and both stores' reports; with the app's, the attribution partner's, the networks' and the stores' records written as those systems write them (`generator/core.py` is the process and the generator writes its arrays to files).
Behaves like the real thing: client-side receipt sync leaves store charges unrecorded for subscribers who stop opening the app (a known gap of apps without server notifications); forgotten store subscriptions keep paying for months, and a checkout that emails a receipt for every charge loses them sooner; about three in ten iOS users allow tracking and they are the more engaged; an ad network optimises delivery on the conversion signal it gets back, so the installs it buys without one convert and retain worse, more so on feed networks than on search or intent ones; a privacy-preserving install postback carries a coarse early value, a campaign and no user; a small team runs its networks market by market in flights; a budgeted campaign spends less of its budget when the auction is dear; a larger budget reaches into wider and weaker inventory; the networks' own install counts run above the postbacks.
Genuine patterns: (1) seasonality: January installs come in larger numbers and less engaged, August smaller, and planned spend follows the season (2) scale: installs rise less than in proportion to a budget (elasticities 0.62 to 0.82) and a larger budget brings less engaged people (3) cohort decay: monthly charges thin month by month, at about 0.91 a month while a subscriber still opens the app, 0.88 once a web subscriber stops and 0.97 once a store subscriber stops (4) the trial: most first charges come on the seventh day, and conversion rises with the first two days' use and with how reachable a person lets an app be (5) auction weather: each channel's delivery share moves week to week with some persistence (6) market mix: Spain is about 60 per cent of installs, Italy 25 and Portugal 15, each channel tilted its own way, and VAT differs by storefront (7) signal: within every paid channel on both platforms the installs that declined tracking are worth less at the same first two days, least so on search and intent channels
Problems by process: the partner's SDK re-sends rows after a retry; reinstalls on second devices; staff and test accounts with sandbox charges; Apple's Pacific days against UTC; postbacks three or four days after the install; view-through credit in the networks' own counts; refunds in both the stores' reports and the records; the budget sheet rounded to ten euros; trailing delivery billed after a campaign is paused
Breadth: twelve or more files; 748,034 consumer accounts (405,661 on iOS, 273,830 of them with no channel), about 0.5 million billing events, 297,131 install postbacks, two stores' daily reports, 104 weeks of budgets and spend on eight channels and their campaigns in three markets, two documents and two or more distractors; ten sources of installs, 32 first-48-hour values, 156 market-weeks and 25 months of store excess, so which slice rules on which estimate is itself work

## Template check

Chain signature: missingness-measurement, decomposition-attribution, causal-reasoning, forecasting, forecasting, modeling, synthesis
Question form: which (which band each channel sits in)
Nearest build: task4 and task24 share the answer shape and the weight (`guard.py check task1`, template.chain_near, a WARN): task4 forecasts a container fleet's 2027 order from loss streams and task24 a label purchase from a classifier's error, each a single forecast with its range; here seven channels are each placed against two lines on a forecast return whose three parts come from three different pairs of records, the chain opens on a missing-charges result, runs through an apportionment and a causal response before any forecast is made, and no build on file shares the chain of areas

## Frontier check

Precedents: R1 careful Missed on L44 (the level read off detailed records instead of the complete summary source) and N21 (an unmeasured component placed across the system in proportion to the metered quantities); R2 Missed on L53 (the selection seen, the unlabelled majority never estimated), N27 (a second record at another grain set aside because it lacks unit identities) and L58 (recording conditions tangled with who the units are read one at a time, no joint fit run); R3 Partly and R6 Missed on L51 (the most rigorous standard design the pack affords, whose own placebo cannot see the difference), L37 (a factor certified by a held-out error that cannot see its bias) and L28 (the estimator certified with checks that cannot see the problem); R4, R5 and R7 Missed on N21, L53 and L51 together.
Shallow path checks: the true-up reconciles the records to the stores' reports exactly in every month, so its control-total check passes; only the web checkout's subscribers, whose charges after the last open are on file, refute it (13.59 against 31.79 per subscriber on AppLovin Android), and only the stores' renewal excess by month refutes a continuation read off the records (the web checkout's takes in 56 per cent of it, the one the app saw 65 to 68 per cent, the fitted one all of it with a monthly error of 23 to 30 renewals, where the other two miss a month by 1,416 to 1,923 on Google Play). The named installs' pricing reconciles each network's installs to its postbacks cell by cell and reproduces the named installs' revenue, and the one labelled iOS channel confirms a correction of about a tenth; only the accounts with no channel (priced at 1.41 times what they paid at the named value and 1.21 at Apple Search Ads' ratio) and Android's named declined installs (4.50 against 3.29 on AppLovin Android) refute it, and only the fit across market-weeks refutes a ratio borrowed for every network (the fitted ratios against Apple Search Ads' 352.6 on five degrees of freedom, against the Android look-alikes' 90.1, against one common ratio 122.9 on four; the 5 per cent points are 11.07 and 9.49). The response on spend beats the budget alone on held-out weeks (10.0 against 20.6 per cent on every fourth week, 12.5 against 22.3 on the last quarter), because the auction moves spend and installs together in held-out weeks too; only the weeks the team moved a budget, each move left out of the fit, refute it (1.872 against 1.403 on Google Android; 13.1 against 3.5 per cent of installs missed across the 286 moved weeks).
Assumption made false: the stores' excess is spread like the recorded charges (false: it belongs to subscribers who stopped opening the app, whose unrecorded charges are a tenth to 36 per cent of a channel's revenue; tested by the web checkout's charges in the billing records and by the stores' excess month by month); the named installs, corrected by the one labelled channel, stand for every network at the same first-48-hour value (false: what a network can do without the signal differs by network, so a declined install is worth 0.44 of a named one on Meta iOS and 0.90 on Google iOS; tested by the accounts with no channel across market-weeks and by Android's named declined installs); the response of installs to spend is what more spend buys (false: spend is the platform's delivery of a budget in that week's auction; tested by the budget sheet's moved weeks).
Forcing: the lines are 0.90 and 1.20. Across the 32 variants the nearest approach to a line is AppLovin Android at 0.951 (the delivery share from the last 52 weeks), 0.051 over 0.90, then Meta iOS at 1.078, 0.122 under 1.20, Google Android at 1.026 and Google iOS at 1.405, with every variant on the golden's side for all seven channels. The shortcuts land across a line: S1 lost puts AppLovin Android at 0.736 (0.778 with one factor per store, 0.847 at the web checkout's continuation, 0.881 at the cancellations the app saw, the nearest of them at 0.019 under 0.90); S2 lost puts Meta iOS at 1.735 (1.561 at Apple Search Ads' ratio, 1.384 at one ratio, 1.303 with organic pinned, 1.280 at the Android look-alike's, 1.204 with the four social networks sharing one fitted ratio, the nearest at 0.004 over 1.20 and refused by the fit's own test at 74.0 on three degrees of freedom); S3 lost puts Google Android at 0.852 (0.813 on the two years' average). `generator/core.py --explore` prints 24 perturbations of the golden route, each holding the call: the share of trial-end candidates charged, the monthly lapse of a subscription nobody opens, each of the six fitted ratios, every channel's budget elasticity of installs and every channel's value slope, each a fifth higher and a fifth lower (the thinnest are Meta iOS at 0.945 and 1.156 with its own ratio moved, 0.045 over 0.90 and 0.044 under 1.20, and Google Android at 0.963 with the elasticities a fifth higher); and the delivery share that turns the plan's spend into a budget moved by 9.6 per cent either way, the widest departure of any channel's quarter from its 104-week share (AppLovin Android 0.916 and 1.034), and taken from the last 26 and the last 13 weeks (0.962 and 0.981; Google Android 1.005 and 0.996). The delivery share is a ratio of two recorded totals, not a fitted quantity (its two years differ from the 104 weeks by 3.6 per cent at most, its halves by 6.9, its quarters by 9.6): moved a fifth lower every call holds, and it would have to be 12.7 per cent higher than any 104-week figure for AppLovin Android to cross into cut (0.864 at a fifth higher).
Noun swap: nearest on file by `skeleton.py check task1`: severity none against every card, the client's corpus and the slot's lineage; task22 v2 and task16 v4 share record_algorithm_inversion, one detection and one move, with a different decision form, answer pattern and mechanisms, and a file-role overlap of 0.25 and 0.12; swapping either build's nouns in carries one lesson of three across and nothing else. Against this slot's own architecture 6 the deciding lesson is new, the decisive rung of the second step moved from one ratio to a joint fit, and the card's differentiation line says so.
Closed strategies: the call turns on unlabelled_pool_apportioned_by_varying_mix, an open lesson (`skeleton.py closed task1`: 0 of 3 lessons closed, no closed supporting step). S2, read by its fix against the nearest cards (self-selection into exposure; a source calibrated on checked cases; groups recorded less completely, grossed up by completeness): the completeness gross-up is the hurried route (every postback at the named value, 45 on the rubric) and the calibration on checked cases is the rigorous standard route (Apple Search Ads' labelled ratio, Meta iOS 1.56, 56 on the rubric); what is estimated beyond both is one ratio per source, fitted together from how the pool's revenue moves as each source's declined count moves across 156 market-weeks, with no checked sample that hands a network's ratio over. S1 (record_algorithm_inversion, next to the completeness card and the reporting-lag card): the stores' reports are the independent total and the gross-up by it is the hurried route (one factor per store-month 44, one per store 43); beyond the card's fix the missing charges never arrive however long one waits, they are assigned to the accounts that could have taken them, and two rates are fitted to the excess month by month and carried account by account, so the correction differs by channel from a tenth to 36 per cent; the rate a checked sample would hand over (the web checkout's continuation) is a priced shortcut that leaves AppLovin Android in cut (0.85). S3 (endogenous_supply_instrument, next to the attenuation card and the margin card): here the slope on spend is steepened, not flattened, by a regressor the outcome's own process sets, and the fix is the team's budget as the instrument with the delivery beside it; valuing at the margin is done by every route including the hurried one (R6 asks for the next euro by name), and the plan's and stretch budgets sit inside the budgets on record, so neither the margin card nor the extrapolation card decides anything. No closed lesson is kept even as a supporting step: the twelve-month value is read on install weeks whose twelve months are on file, so no young cohort is completed.
Decisive steps: S1 owns AppLovin Android's twelve-month net revenue per install for the installs bought in the year to 2 November 2025, EUR 4.87 (4.83 to 4.91), asked for by "the 12-month net revenue in euros per install of the installs each channel bought in the year to 2 November 2025" and carried in the CSV's row and the workbook; its evidence is the stores' daily reports (units by product, event and storefront) against the billing events' transaction dates and each account's last open, plan and renewal setting as last seen; once named, four steps are left. S2 owns Meta iOS's figure under the same words, EUR 5.78 (5.67 to 6.00); its evidence is the postbacks' campaign, arrival day and first-48-hour value, each account's tracking answer, storefront and channel on file, and the billing events; five steps left. S3 owns the installs a week the plan's spend buys on Google Android, 611 (596 to 627), asked for by "how many installs a week the plan's spend will buy"; its evidence is the budget sheet's weekly budgets and the platforms' daily spend beside the installs by week; three steps left. Independence, from corelib's lattice (component by component, then the call): S1 left out alone 3.70, 5.78, 611 and AppLovin Android cut (0.74); S2 alone 4.87, 9.55, 611 and Meta iOS scale (1.73); S3 alone 4.87, 5.78, 511 and Google Android cut (0.85); S1 and S2 out 3.70, 9.65, 611 with Meta iOS scale and AppLovin Android cut; S1 and S3 out 3.70, 5.64, 511 with Google Android and AppLovin Android cut; S2 and S3 out 4.87, 9.55, 511 with Meta iOS scale, Google Android cut and TikTok iOS and Snapchat iOS hold; all three out 3.70, 9.65, 511 with Meta iOS scale and both Android channels cut. Each component is earned whenever its own step is made, whatever happens to the other two.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | an install | a new consumer account's first install; every install row; every postback | a new consumer account's first install | growth policy 2.2 (a second device, a reinstall, staff and test accounts are not installs) |
| SF2 | the installs a channel bought | the installs the export names; the networks' own counts; the postbacks for the iOS networks and the channel on file for the others | the last | growth policy 2.2 (each install bought by at most one channel, whether or not the partner can name it); the networks' own counts credit view-throughs and sum above the accounts |
| SF3 | twelve-month net revenue | every charge made in the 365 days from the install; the charges in the billing records; twelve calendar months | every charge made in the 365 days | growth policy 2.3 (what the stores and the checkout charged) |
| SF4 | net of what | VAT, the stores' commission and the checkout's fee; VAT only; the stores' proceeds as reported | VAT by storefront, 15 per cent commission, 3 per cent fee | growth policy 2.4; the stores' proceeds agree with it |
| SF5 | the return at the plan's weekly spend | the 52 weeks' revenue over the 52 weeks' spend; the mean of 52 weekly ratios | the 52 weeks' revenue over the 52 weeks' spend | growth policy 2.1 (the period's revenue over the period's spend) |
| SF6 | the stretch spend | the plan's stretch column in every week; a single uplift on the year | the stretch column in every week | media_plan_2027.xlsx (a stretch spend beside each week's plan spend) |
| SF7 | what one more euro returns | the change in twelve-month net revenue per extra euro at the plan's spend, every week raised in the same proportion; the plan-to-stretch average | at the plan's spend | growth policy 2.6 |
| SF8 | the net revenue per install the plan's spend buys | the 52 weeks' revenue over the 52 weeks' installs; the mean of weekly values | revenue over installs | growth policy 2.1 and 2.3 (the installs a period's spend buys and what they were charged) |
| SF9 | a return on a line | 0.90 holds, 1.20 scales; the reverse | from 0.90 hold, from 1.20 scale | growth policy section 3 |
| SF10 | the channels placed | the channels of the media plan's growth sheet; every paid channel in the records | the plan's growth channels | growth policy section 1 and the plan (Apple Search Ads sits on the fixed brand budget, which the policy does not place) |
| SF11 | a charge's day | the store's transaction time; the time the app recorded it | the transaction time | growth policy 2.3; charges recorded late carry their transaction time |
| SF12 | refunds | netted; ignored | netted | growth policy 2.3 |
| SF13 | the installs a week the plan's spend buys | the plan year's installs over its 52 weeks; the installs of an average week of the record | the plan year's installs over 52 | the prompt's own words and the media plan's 52 weekly spends |
| SF14 | the installs each channel bought in the year to 2 November 2025 | the installs of the 52 weeks from 4 November 2024 to 2 November 2025, whether or not the export names them; the named installs of those weeks | every install of those weeks | growth policy 2.2; those are the weeks whose 365 days are on file by 8 November 2026 |
| SF15 | an iOS account with no channel | organic; an install nobody could name | an install nobody could name | the export gives the organic label only to accounts that allowed tracking, and each network's postbacks outnumber its named installs by more than three to one |
| SF16 | a postback's install week | its arrival day; its arrival less three days; less four; half the count three days back and half four | half and half | skadnetwork_conversion_values.json (a 48-hour window and a postback 24 to 48 hours after it closes); same call with three days and with four (two of the 32 variants) |
| SF17 | the first-48-hour value's cells | the 32 values; eight or four groups; cells of fifty or more; each source's named installs through one tilt | the 32 values, a source's cells under 20 named installs through its own level | same call (four of the 32 variants) |
| SF18 | the weeks the response is read on | the 104 weeks to 1 November 2026; without the launch quarter; the last 78 weeks | the 104 weeks | same call (two of the 32 variants) |
| SF19 | the weeks the delivery share is taken over | the 104 weeks; the first 52; the last 52; the last 26 or 13 | the 104 weeks | same call (two of the 32 variants, which set the installs-a-week ranges; the last 26 and 13 weeks in the perturbation table of `core.py --explore`) |
| SF20 | the share of trial-end candidates charged | by store, spread by how trial starters of the same first two days went on to buy; one share for every candidate; one fit across both stores | by store, spread by first-48-hour use | same call (two of the 32 variants) |
| SF21 | the continuation of a subscription nobody opens | one rate by store fitted to the stores' renewal excess month by month; two rates; the fit without its last two months; a thirty-day cadence; the web checkout's continuation; the cancellations the app saw per charge on file | one rate by store, fitted (0.972 Google Play, 0.970 App Store) | same call for the three fitted ways (three of the 32 variants); the web checkout's 0.878 takes in 44,840 of Google Play's 80,168 excess renewals and 44,137 of the App Store's 78,809, and the rate the app saw (0.912 and 0.905) 54,435 and 51,493, where the fitted rates take in 80,428 and 78,664 with a monthly error of 30 and 23 renewals (on Google Play the web checkout's rate misses a month by 1,923 and the rate the app saw by 1,416) |
| SF22 | how each source's ratio is fitted | market by week, weighted by one over the accounts in the market-week; unweighted; weights from the fitted revenue; by fortnight; by four-week period; market-weeks of fewer than a hundred accounts left out; separately for lighter and heavier first-48-hour use; drawn toward the pooled ratio by the fit's own spread; organic's ratio taken from Apple Search Ads | market by week, weighted | same call (nine of the 32 variants) |
| SF23 | which sources may share one ratio | none; Google iOS with Pinterest iOS, either with the organic installs, or all three; Meta with TikTok; TikTok with Snapchat; Meta, TikTok and Snapchat; the four social networks; every source | none | same call and inside the ranges for the four groupings the fit's own spread cannot tell apart (2.87, 0.02 and 1.14 on one degree of freedom against 3.84, 3.01 on two against 5.99; four of the 32 variants); the others are refused by the same test (Meta with TikTok 4.43 and TikTok with Snapchat 4.49 against 3.84, the three 17.5 against 5.99, the four social networks 74.0 against 7.81, the five networks 122.9 against 9.49), and the first three of those still file the golden call |
| SF24 | a declined install's worth taken from another source | the named installs' value; Apple Search Ads' labelled ratio; the ratio the network's kind shows on Android; the pool's own value by first-48-hour value | none of them | the accounts with no channel priced that way add up to 1.41 times what they paid at the named value and 1.21 at Apple Search Ads' ratio, against 1.00 fitted; the fitted ratios stand 352.6 from Apple Search Ads' and 90.1 from the Android look-alikes' on five degrees of freedom (11.07); on Android, where the declined installs are named, AppLovin's paid 3.29 against 3.55 fitted, 4.50 at Apple Search Ads' ratio and 5.26 at the named value |
| SF25 | what the response is fitted on | the budget with the delivery beside it; spend instrumented by the budget; the budget alone; the week's spend; the two years' average return | the budget with the delivery beside it | same call for the first three (two of the 32 variants); the fit on spend misses the installs of the 286 moved weeks by 13.1 per cent, each move left out, against 3.5, and files 1.872 for Google Android's raised over lowered weeks against 1.403 |
| SF26 | the month pattern, the value response and its slope | one pattern across channels and each channel's own slopes; each channel's own pattern; one value slope across channels; the value response on the mature weeks' own values | one pattern, own slopes, the value by first-48-hour value over all weeks | same call (three of the 32 variants) |
| SF27 | a week's month in the month pattern | the month of its Thursday; of its Monday | its Thursday | media_plan_2027.xlsx (its weekly spend changes on the weeks whose Thursday falls in a new month); the Monday reading is asserted to file the same call on the cut pack |
| SF28 | the period the stores' reports and the billing records are compared on | periods of 30.4375 days from 4 November 2024; calendar months | the 30.4375-day periods | same call, asserted on the cut pack (the comparison is a sum over the same charges either way) |
| SF29 | the day of an App Store report row | the Pacific day its `date_pt` column names; a UTC day | the Pacific day | appstore_subscription_events_daily_2024-11_2026-11.csv (the column is `date_pt`); the UTC reading is asserted to file the same call on the cut pack |
| SF30 | a refunded purchase in the stores' reports | taken out on the day it was charged; netted on the day of the refund; netted from the renewals | the day it was charged | same call, asserted on the cut pack |
| SF31 | the clock an install's 365 days and install week run from | the account's `created_at`; the attribution export's `install_time` | the account's `created_at` | same call, asserted on the cut pack (the export's install time is the app's first open, a minute or so before the sign-up and never after it) |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| VAT by storefront | 21, 22, 23 per cent | growth_policy_paid_channels_v3_2026-09.pdf, 2.4 |
| the stores' commission and the web checkout's fee | 15 and 3 per cent | growth_policy_paid_channels_v3_2026-09.pdf, 2.4 |
| prices and the trial | EUR 9.99 monthly, EUR 59.99 annual, seven days | growth_policy_paid_channels_v3_2026-09.pdf, 2.5; the billing events' own prices in billing_events_2024-11-04_2026-11-08.csv |
| the lines | 0.90, 1.20 | growth_policy_paid_channels_v3_2026-09.pdf, section 3 |
| the plan's weekly spend and stretch spend | 52 weeks by channel | media_plan_2027.xlsx |
| the first-48-hour value and the postback's timer | 32 values; 48 hours, then 24 to 48 hours | skadnetwork_conversion_values.json |
| the billing cadence | a month of 30.4375 days | measured on the billing events in billing_events_2024-11-04_2026-11-08.csv; spread with a 30-day cadence in the battery |
| the share of trial-end candidates the stores charged | 0.034 and 0.030 monthly, 0.041 and 0.034 annual (Google Play, App Store) | fitted to the stores' first-charge excess in the two store reports (.csv); measured spread across one fit for both stores, one share for every candidate and the last two months left out |
| the monthly continuation of a subscription nobody opens | 0.972 and 0.970 (Google Play, App Store) | fitted to the stores' renewal excess in the two store reports (.csv); measured spread across two rates, a 30-day cadence, the last two months left out and one fit for both stores |
| each source's ratio of a declined install's worth to a named one's | Meta iOS 0.435, TikTok iOS 0.517, Snapchat iOS 0.614, Google iOS 0.898, Pinterest iOS 0.808, organic 0.888 | fitted across 156 market-weeks from accounts_2024-11-04_2026-11-01.csv, skan_postbacks_2024-11-07_2026-11-05.csv and the billing events; each ratio's own standard error (0.029 to 0.047) and the measured spread across the battery's nine fits and four groupings |
| the named installs' value by first-48-hour cell | by source, a source's own cells of 20 named installs or more | accounts_2024-11-04_2026-11-01.csv and the billing events; measured spread across eight and four groups, cells of 50 and one tilt per source |
| a postback's install week | arrival less three days and less four, half the count each | skadnetwork_conversion_values.json (the timer); measured spread with three days and with four |
| each channel's budget and delivery slopes, the month pattern | fitted | paid_budgets_weekly_2024-2026.xlsx and ad_spend_daily_2024-11-04_2026-11-01.csv with the installs; measured spread across each channel's own month pattern, the launch quarter left out, the last 78 weeks, one value slope, the mature weeks' own values, spend instrumented by the budget and the budget alone |
| the delivery share that turns the plan's spend into a budget | each channel's spend over its budget, 104 weeks (0.83 to 0.87) | paid_budgets_weekly_2024-2026.xlsx and ad_spend_daily_2024-11-04_2026-11-01.csv; measured spread with the first 52 and the last 52 weeks |

Variant battery: 32 variants beside the golden in `generator/core.py`, and every variant files the same call for all seven channels: five on the first step (one fit across both stores, a two-rate continuation, the fit without the last two months, a thirty-day cadence, one share charged for every trial-end candidate), eighteen on the second (cells in eight groups, in four groups, cells of fifty or more, one tilt per source; the ratios fitted separately for lighter and heavier first-48-hour use, unweighted, by fortnight, by four-week period, with weights from the fitted revenue, with organic's ratio taken from Apple Search Ads, without market-weeks of fewer than a hundred accounts, drawn toward their pooled ratio; the four groupings the fit cannot tell apart; every postback dated back three days, and four) and nine on the third (each channel's own month pattern, the launch quarter left out, the value response on the mature weeks' own values, one value slope across channels, the delivery share from the mature weeks and from the last 52, the last 78 weeks, spend instrumented by the budget, the budget alone). The ranges of ## Stump core are their span with a quarter of its width each side. On the cut pack the build's analysis adds the conventions only the files carry (SF27 to SF31) and re-sets every range from the whole battery before anything is priced.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the installs each plan channel's 2027 spend buys (R3 to R7); the installs each channel bought from 4 November 2024 to 2 November 2025 (R1, R2) |
| 2 | Unit of account: euros of twelve-month net revenue per euro of spend; installs a week; euros per install; euros per extra euro |
| 3 | Attribution window: the 365 days from each install's day |
| 4 | As-of dating: the exports pulled 9 November 2026, data to 8 November 2026 |
| 5 | Version basis: growth policy version 3 of September 2026; the media plan's draft of 30 October 2026 |
| 6 | Denominator: spend as the platforms bill it; installs as policy 2.2 defines them |
| 7 | Weighting: the plan's weeks weighted by their own spend and installs; the second step's market-weeks by one over their accounts (unweighted and revenue-weighted in the battery) |
| 8 | Window length: twelve months per install; 104 weeks of budgets and spend; 52 plan weeks from 4 January 2027 |
| 9 | Boundary inclusivity: an install on 2 November 2025 is in the mature year; a charge on day 365 is out |
| 10 | Rounding path: every figure at full precision to the end; returns stated to two decimals, installs a week to the unit and euros per install to the cent in the answer blocks, each with its range |
| 11 | Tie-break: none needed; the nearest channel to a line under any variant is AppLovin Android at 0.051 over 0.90 |
| 12 | Maturity and censoring: the mature year's twelve months are complete by 8 November 2026; later weeks enter through their first-48-hour values only |
| 13 | Order of operations: installs by channel, the charges the records never took in, each source's ratio and the unnamed installs' value, the response to the budget, the plan and stretch spends, the bands |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: a re-sent export row (same install id) counted once; a reinstall is not an install |
| 16 | Identity normalisation: one account id across the accounts, the billing events and the export; postbacks carry a campaign and no account |
| 17 | Netting against gross: refunds netted; VAT, commission and fee taken off |
| 18 | Dimensional units: euros, VAT included in the price charged; weeks Monday to Sunday; a market is a storefront (ES, IT, PT) |
| 19 | Code and status semantics: production charges only; consumer accounts only; the first-48-hour value as the schema file maps it; a campaign runs in one market |
| 20 | Integerisation: none; installs a week stay fractional in the forecast |
| 21 | Clause scope: the bands apply to the 2027 plan's growth channels at the plan's weekly spend; the stretch spend is a figure, not a second call |
| 22 | Forward window contents: the media plan's 52 weekly spends and stretch spends; prices unchanged (policy 2.5) |

## Literal reader

Executing the shipped sentences word for word: policy 2.1 makes a channel's return the twelve-month net revenue of the installs a period's spend buys, per euro of that spend; 2.2 makes an install a new consumer account's first install, bought by at most one channel whether or not the partner can name it; 2.3 counts every charge the stores or the checkout made in the 365 days from the install, at its transaction time, net of refunds; 2.4 takes off VAT by storefront, the stores' 15 per cent and the checkout's 3 per cent; 2.5 files the prices and the seven-day trial; 2.6 makes the marginal return the twelve-month net revenue an additional euro of spend returns at a stated spend, every week raised in the same proportion; section 1 places the channels of the plan's growth sheet; section 3 cuts under 0.90, holds from 0.90 and scales from 1.20. The media plan gives each growth channel 52 weekly spends and stretch spends. The prompt asks for each channel's return at the plan's weekly spend and at its stretch spend, the installs a week the plan's spend will buy with their twelve-month net revenue per install, what one more euro on top of the plan's weekly spend returns, and the twelve-month net revenue per install of the installs each channel bought in the year to 2 November 2025. Executed literally these fix what every figure is; none says how the charges the records lack, the installs the export does not name or the installs a budget buys are to be estimated, and a reader who follows the prompt's words and estimates each figure the golden's way lands on the golden.

## Prompt contract

A voice rewrite may not drop or change: the question (which band each paid channel of the 2027 media plan sits in under the growth policy), the plan's weekly spend as the basis, why the answer must be an estimate (none of the installs is twelve months old before 2028; the records end 8 November 2026), "a committed figure" for every channel, the four asks with their units (the 2027 return in euros of 12-month net revenue per euro of spend at the plan's weekly spend and at its stretch spend; how many installs a week the plan's spend will buy and the 12-month net revenue in euros per install of those installs; what one more euro on top of the plan's weekly spend returns in euros of 12-month net revenue; the 12-month net revenue in euros per install of the installs each channel bought in the year to 2 November 2025), and the two deliverables by type (a workbook with the bands on its first sheet, the channel figures as a CSV). It must never add: a method, a comparison or an adjustment, a file name, a role, a rounding rule, a count of channels, or any word about tracking, consent, the stores' reports, campaigns, markets, budgets or auctions.

## Build brief

World: Zancada Fitness S.L., a Spanish home-workout subscription app sold in Spain, Italy and Portugal (EUR 9.99 monthly, EUR 59.99 annual, a seven-day trial), 104 install weeks from Monday 4 November 2024 to 1 November 2026 and exports pulled 9 November 2026. `generator/core.py` is the process: the generator calls `core.simulate()` (SEED 71126 for the people, BUDGET_SEED 71116 for the budgets and the auctions, CAL_SEED 7360 for the campaign flights) and writes its arrays as the systems would (the app backend's accounts and billing events, the attribution partner's export, the networks' install postbacks, the App Store's and Google Play's daily reports, the ad platforms' daily spend by campaign, the growth team's budget sheet and the 2027 media plan), then lays the Layer 1 mess on the files without touching an array the core reads. Every paid channel but Apple Search Ads runs one campaign line per market, live in the weeks `CH[c]["live"]` says, and an install's market is its storefront.
Frozen: everything in `generator/core.py`: the three seeds, the dials of CH and ORGANIC (the members, their budgets, plan and stretch factors, moves and flights), CONSENT, CONV, DORMANT0, DORMANT, CHURN, CHURN_SILENT, CHURN_SILENT_WEB, GAP, the delivery constants, LINES, PB_ALIGN, the golden estimators (`s1_fit`, `s1_values`, `s2_cells`, `s2_strata`, `s2_fit`, `ios_price`, `response`, `at_plan`), HURRIED, RIGOROUS, the 32 VARIANTS, the three referees, FAMILIES and COMPONENTS (the 39 ask figures and the three components, one per step). The build's analysis reads the files back into the arrays `Obs` holds and must reproduce the core's figures; it adds to the battery only the conventions the files carry (SF27 to SF31) and re-sets the ranges from the whole battery. A gate that cannot pass inside these, a file-level convention that moves a call, or a one-step-lost route over 50 on the cut pack comes back to the draw.
Files: accounts (one row per account: creation time, platform, storefront, the tracking answer, the first-48-hour value, billing route, plan and renewal setting as last seen, trial state as last seen, last open; never the person's traits, the wide inventory or the source of an unnamed install); billing events (every charge the app has on record with its transaction and recording times, store charges up to each account's last open and every web-checkout charge: the web checkout's subscribers are S1's referee and ship whole); the attribution export (install rows with the channel and campaign where the partner could name them: every Android install whatever the tracking answer, every Apple Search Ads install, iOS installs whose users allowed tracking, the organic label on iOS only for accounts that allowed tracking; Android's installs that declined tracking, named with their channel, are S2's referee and ship whole); install postbacks (one row per install of the five iOS networks: arrival date, network, campaign, first-48-hour value, no account); the two stores' daily reports (units and proceeds by product, event and storefront, no account); daily ad spend by channel and campaign (spend, impressions, clicks, the network's own install count; a channel's campaigns sum to the core's weekly spend to the cent); the budget sheet (the weekly budget the team set per channel, one line per channel, with its notes on each move, the moved weeks being S3's referee); the media plan (52 weekly spends and stretch spends for the seven growth channels, the fixed brand budget on its own sheet); the growth policy (PDF from a word processor); the conversion-value schema (JSON); two or more unlabelled distractors. Two CSVs of 20,000 rows or more and a pack of 30 MB or more. No file carries a return, a value per install, a ratio by network or a ranking of channels, and no data dictionary ships.
Never filed: that a store charge is recorded "only when the app is next opened" or "at the next sync"; "dormant", "silent" or "forgotten" subscribers; any continuation or churn rate; that users who decline tracking "are worth less", "convert worse", "are lower quality" or were "bought blind"; "signal loss", "modelled conversions" or an "adjustment factor" by network; "unattributed installs include paid installs"; that flights or dark weeks help measure anything; "delivery", "pacing", "underspend" or "the auction" as a reason spend differs from budget; "budget is what we control"; any column named for a stump (no dormant flag, no wide-inventory flag, no auction index, no true channel on an unnamed install); any sentence telling which record to trust for what; file names that name a problem.
Goldens: `paid_channels_2027.xlsx` (first sheet: each channel's band with its return at the plan's spend and at the stretch spend, the installs a week and the net revenue per install the plan's spend buys, what the next euro returns and what the installs of the year to 2 November 2025 went on to pay, with a chart of the returns against the two lines; behind it the charges the records never took in by store and channel, each source's ratio with the adding-up by market and the Android check, the response to the budget with the moved-weeks check, and a routes sheet setting the hurried choices beside the estimates) and `paid_channels_2027.csv` (one row per channel: the six asked figures and the band). Every figure from `generator/figures.json`; the three components (one line each, the answer with its unit and range and no method) and the Step-by-Step counts in `submission.md`, whose Supplementary Questions carry four numbered entries, one per ask.
Free: file names and column names beyond the words above, the campaigns' names and creatives, how a channel's weekly spend is split across its live campaigns and days, the Layer 1 mess and its sizes, the distractors, the policy's wording outside sections 1 to 3, the budget sheet's notes (reasons a team gives for moving a budget or pausing a market, never the auction), the workbook's layout behind its first sheet.

## Tried and rejected

- Matching new members to the tutor with the most open slots (pricing simulator v1 to v2): every month's new members
  went mostly to new tutors, so history carried the same exposure as AUT26 and the curve landed on the truth
  (0.834 against 0.837 of receipts); the world needs the platform to match new members to established tutors and to
  run with spare established capacity, which it does.
- Twelve-month receipts per member as the decision quantity: the four observed months dilute the move to about
  3 per cent of the figure; the twelfth-charge retention carries it at about 18 per cent.
- Matching new members to the most established tutor with room, where "established" began at four teaching months
  (simulator v9): surge members landed on tutors inside the stopping hump, the spring 2025 campaign carried as much
  exposure as AUT26 and the curve missed it by 17 to 22 per cent on back-test, a search signal; established now means
  nine or more teaching months.
- A spring 2025 campaign of 680 members (simulator v7 to v10): either it carried most of the effect (the textbook
  route failed its own back-test) or it was too small to tell the models apart; SPR25 is now 264 members, too few to
  separate the routes on its own, the textbook route validates on it, and the discriminating evidence is member-level.
- Tutor capacity fixed at hire (generator v1 and v2): established tutors stayed full, so surge and growth overflow
  went to tutors inside the hump in ordinary months, history carried AUT26's exposure and the curve landed near the
  truth (0.301 against 0.303); established tutors now open more slots once past their first nine teaching months.
- A post-rematch uplift and calendar-month seasonality in the process (generator v3 to v6): neither decided anything,
  and between them they moved the graded cost per twelfth-month member by about 1.3 per cent across defensible
  variants, a fork at any useful rounding; both left the process.
- A 50 per cent first-month offer: the discounts were a quarter of the cost, so a deep run that misread the cost rule
  and left them out filed the re-run; the offer is now 10 per cent and leaving it out stays 5 per cent outside the bar.
- Tutor ids rewritten at a 2025 lesson-platform migration: left unnormalised they split tutors, flattened the stopping
  hump and flipped the call (1,274 twelfth-month members), so cleaning decided the answer; ids keep one format.
- A range on the twelfth-month members as an ask: tutor-clustered and member-independent ranges coincide at the
  nearest 50, so it graded no judgment; the cost ranges at the nearest 25 separate at every endpoint.
- Fuller new-tutor rosters to widen the clustered range (caps 26 to 36): one endpoint separated and the shallow routes
  moved to within 6 per cent of the bar; reverted.
- A 95 per cent range on the cost per twelfth-month member: its upper end sat on its rounding line at 4,000 draws
  and its lower end moved with the draw, so the figure was a coin at the nearest 25; the 90 per cent range keeps both
  ends inside their rounding (`checks.py` R7) and members drawn one at a time move both ends.
- An 80 per cent band on each month's total in the workbook: several of its 22 ends changed between seeds at 4,000
  draws at the nearest 50, and at the nearest 100 it no longer told tutor-by-tutor draws from member-by-member ones;
  the workbook carries the monthly expectations only.
- 2026-11-09, architecture 1 (Corvane, the autumn campaign's members carried through their tutors' stopping hump):
  returned in kind by the project lead's review (one hidden constructed factor; the forward cohort was the only one
  built to be exposed, the generator tuned until history stopped carrying the exposure, and every graded figure came
  from one projection). Re-rooted to a new world as a results chain.
- 2026-11-09, stage 3: seat additions from the book's mean growth in users by account age (no account's own drift):
  EUR 0.10 million against the process's EUR 0.49 million, because need growth differs by account and seats only
  ever true up; replaced by each account's own drift, shrunk to the book (24 months), with 12 and 18 months, each
  account's trailing true-up rate and the book's trailing rate kept as rivals.
- Each account's trailing true-up rate as the golden's seat additions (the stage-2 prototype): EUR 0.56 million,
  above every drift form; kept as a rival, inside every band.
- A slower April decay (PAD_DECAY 3.0, PAD_SHOCK 0.10) to push the careful pass's last-three-months Team rate out of
  R3's band: the excess series is too noisy month by month for the golden to tell the forms apart either, and the gap
  stayed about EUR 15,000; parameters reverted, R3 priced Partly for the careful pass.
- The commitment graded at one 0.1 million bin: the honest family's P20 spans EUR 9.79 to 9.92 million (the exit
  model's utilisation form and the seat-addition form move it), so the commitment's band is 9.8 to 9.9 and the draft
  moved from EUR 10.4 to 10.2 million so that the careful pass (10.23) still clears it wrongly.
- The draft at EUR 10.4 million: the careful but hurried pass's commitment (EUR 10.2 million) sat under it, so the
  pass gave the right verdict for the wrong reason; the draft is EUR 10.2 million.
- Credit notes and re-issues on renewals after 1 March 2026: kept beside the re-issues they moved the price line to
  EUR 310,000 and the commitment to 10.0, so cleaning decided R2; the billing errors now sit on 2024 to February 2026
  renewals, where kept they break the renewal pairing visibly and decide nothing.
- The workspace links' end-and-restart dates listed as Layer 1 mess: read without dates they move R3 (1.43), R5
  (1.12) and the commitment (9.7), because the dates are how an upgrade is told from a cancellation; they are
  evidence for R3, R4 and R5, not mess.
- The ask "how much of October's Team ARR is still billed on the Team plan in December 2027": read two ways (the
  October ARR of the accounts still on Team, or their December 2027 ARR, about EUR 0.07 million apart); the prompt
  now asks for the Team ARR in December 2027 from accounts on the plan at the end of October 2026.
- New Business accounts held at their signing ARR to December 2027 (their ramp true-ups and the first renewals of
  November and December 2026 signings ignored): policy 4.2 counts a first term at its service start, every route
  shares the convention, and it is recorded rather than modelled.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, architecture 2 after the holistic-audit repair (seed 1126; commitment the largest EUR 0.1 million step met in 80 per cent of outcomes, 10.0, met in 83 per cent, 10.1 in 69; draft 10.3, met in 36; every naive extrapolation 10.72 to 11.49 clears it; judge DETERMINISTIC APPROVE): measured against the uploaded platform run's own methods (price by size, renewals on utilisation and first renewal, pipeline by stage and time in stage, the Team plan's last three months, recent deal creation), the run lands the commitment and earns R1, R2 and R5, scoring 66.5 of the 93 graded weight (R3 and R7 missed, R4 partly); its two blind spots cancel (lost accounts about 130,000 low without the group term, Team about 76,000 low on the autumn peak). Two world moves were measured and rejected: the Team cancellation peak moved to late winter shifted the golden as far as the route (commitment 10.2, the draft met in 78 per cent); the seat-growth spread restored to the uploaded world's (0.08 a year, monthly noise 0.008) brought back the run's seat-addition miss (routes on pooled rates at 9.8 and 9.9) but spread the honest family over two steps (10.0 and 10.1). The routes table shows why: the five designed judgments each move the 80 per cent figure of a 10 million book by 0.0 to 0.15 million, inside the honest family's own spread, and only the CRM's odds (10.73), independent draws (10.39) and pooled renewals (10.29) separate, all three moves the uploaded run did not make. The determinism the audit requires (the band's contents filed, no added allowance) removes the stacked pessimism that made the uploaded run miss by 0.7 million. The world is spent: a commitment on one total aggregates every judgment below the methods' disagreement. Re-root to a new world in which each judgment flips units of a set or count.
- 2026-11-10, architecture 3 at the draw, a ranked list under a budget cap (best value per euro first until the next line would not fit): over two million cost and budget configurations searched against every rival, the robust cuts (a 7 to 12 per cent gap, leftover budget fitting no unfunded line) turned on one or two lines (the social Kreisblatt and telemarketing Kreisblatt pair) and a careful run that used the reading log landed the golden list, because the full-price and returns shortcuts cancel on the deep-intro lines; replaced by the standard's line-by-line bar (3.5 times the planned cost per start), on which ten lines sit 3 to 14 per cent from the bar, every rival funds the same eight and the shortcuts fund six distinct wrong sets.
- 2026-11-10, the base's December 2027 count as R9: the October 2026 base is mostly long-tenured, so the careful pass's errors cancel (the rise read late adds 3 to 4 per cent, customer-number returns take 2.5 off) and it lands within half a per cent; replaced by the intro subscribers at the cut carried to the full price in December 2027, which the careful pass misses by 6 to 9 per cent.
- 2026-11-10, a first debit able to fail in the engine: a subscription could end before it began, colliding with the withdrawal code for January 2023; failures now start at the second billing, and the pack reproduces the simulator's panel field for field.
- 2026-11-10, stage 4, R9 as the October 2026 intro subscribers paying full price in December 2027: priced on the rubric split, a careful run that read the April 2025 rise in full earned R6 and R9 together (both asks, both carried by the rise's first-year response) and scored 62.1; R9 is now the plan's 2027 starts still paying on 31 December 2027 by channel, carried by the full price at the end of intro and the newest starts' survival, and that variant scores 48.4.
- 2026-11-11, the platform's holistic audit of the uploaded build (returned on determinism): R9 counted the telemarketing free quarter as paying (498 against about 454 on 31 December 2027; standard 2.2), nine lines sat 5 to 7 per cent from the 3.5 bar and J12 had never run on telemarketing or cashback, so a 20 per cent shift in exit rates moved the call from 7 to 15 lines. Repaired: R9 counts no free month; TEL-BHR ran J12 from May 2024 to February 2025 and PART-GAZ from January to September 2024, so both 2027 J12 lines carry an offer their channel ran; the plan's costs per start re-placed so every line sits 12 per cent or more from the bar.
- 2026-11-11, wider margins on the uploaded world (habit drift 0.65 and 0.50, a full-price coefficient of 2.2): with every line 10 per cent or more from the bar the careful pass's social lines needed two shortcuts together (the reading and the period term, each 9 to 18 per cent), so the reading hint and the full-price hint each rescued the funded set and completion alone flipped nothing; the call would have hung on whichever of the two a run made. The process now carries both more strongly (the newest social starts' habit 0.9 lower, cashback 0.7, a full-price coefficient of 3.0), so each single judgment moves lines past the margin: completion alone funds SOC-KBO, the period term SOC-KBO and APP-KBO, and no hint rescues the set.
- 2026-11-11, a calibration of each line on its own newest starts (observed over expected full-price cancellations, shrunk by a pseudo-count) as a rival: it moves SOC-KBO 24 per cent up and swings 8 to 37 per cent with its own pseudo-count and window, because each line's starts of the twelve months to October 2026 have had 3 to 18 full-price cancellations (139 in all, against 146 the reading model and 138 the channel model expect); the count cannot separate the models, so the rival is ruled out on its data rather than banded, and the closing passage and the Checks sheet name it.
- 2026-11-11, a household bootstrap as the forcing evidence: drawing households ignores the line-month campaigns that move a month's starts together and gave line spreads of 3 to 5 per cent; whole start months are now drawn within each line (boot.py, each copy keeping its own customer numbers, fingerprints and addresses so the links rebuild inside it), spreads 2 to 7 per cent, and 39 of 40 draws fund the same eight lines.
- 2026-11-11, a back-test of the leaving model fitted on the 2024 starts and scored on the 2025 starts as forcing evidence: both models over-predict the later starts' exits (the reading model by 10 per cent, the channel model by 25), so it is not shipped; the reading coefficient (minus 0.69, standard error 0.03, on 2,336 cancellations) and the newest starts' measured reading carry the forcing.
- 2026-11-11, the offer and the price stepped up to as terms in the leaving model: neither improves the fit (AIC 20,339.7 and 20,334.3 against the golden's 20,335.0) and each moves line values 2 to 6 per cent; both are rivals inside the bands.
- 2026-11-12, architecture 3 as reshipped (every line 12 per cent from the bar, the clean truth and 39 of 40 redraws on the golden set): returned on determinism by the platform's review (runs/arch3/review_2026-11-12.md); the household-return projection and the young starts' completion were open modelling choices, and the return hazard fitted without early reading alone funds 9 lines (SOC-KBO 3.52), with channel completion 13 (EUR 127,830); the forcing family had tested each choice only inside the hurried route, never alone; both deciding lessons are on the client's closed page of 2026-11-12; architecture spent, re-rooted to a new world.
- 2026-11-12, architecture 4 drawn on a greater-of remuneration (the larger of 52 per cent of revenue and a per-hour floor, monthly on the service's totals): on paper the floor bound in two to four months within 5 to 9 per cent of the kink, so the regime calendar was an open fork, and the with-and-without increment it priced is a reflex (the architecture 3 run computed paired forecasts unprompted); replaced by a flat 2027 rate per counted hour, the 2026 revenue share kept as the shortcut a run carrying the latest cost files.
- 2026-11-12, at build: an AND built from the live log over-counting Gezin's re-listening: the counting rule takes a title's live position at most once, so a live-only first reach can only under-count (Gezin came out low, not high); the second correction moved to profile membership, partners folding their own subscriptions into family accounts with their history, which today's profile export credits to the family account.
- 2026-11-12, at build: the 2026 revenue share carried forward landed on the golden's plan (Gezin) while Gezin's counted hours per euro of revenue sat near Onbeperkt's; child profiles' listening moved toward re-listening and Onbeperkt's adults listen more, so taking hours out of the cost now favours Onbeperkt, and the agency fees were set from the pack's own pre-fee values over a plausible band (EUR 10 to 55) for the widest narrowest margin (24 per cent on paper, EUR 8.7 measured).
- 2026-11-12, at build: a filed fee perturbation of 10 per cent on Gezin left it EUR 3 ahead and a 10 per cent move in the 2027 rate would flip it to Flex; the rate is filed in schedule B and not fitted, so the forcing block moves the fees 10 per cent and each plan's measured counted hours 5 per cent, and the note records that R5's level is sensitive to the count's level, which the reconstruction pins exactly.
- 2026-11-12, stage 4, architecture 4 as built (Gezin EUR 22.0 per trial start, careful route Onbeperkt, pair 43.7 on paper): the determinism judge kept the order and its own first pass rebuilt R1 exactly and R2 inside the band on all four plans before it opened the blocks, merging the licence renewals and dating profiles by the charges' profile lists by reflex; disposition SEND_BACK on Gate G (planted_defect_flip: a coverage gap and a stale roster, two record corrections whose discovery is their remedy) and H3 and H5 (the compound hint naming both rescues the call); architecture spent. The lesson for the next draw: a second record the pack carries beside a reconciliation target is merged by reflex, so the deciding judgment must be an estimate whose reflexive method lands wrong, not a record to be found or re-keyed.
- 2026-11-12, architecture 5 at design: the cap response graded as a result: its estimate from counted hours (1.6) cannot recover the world's multiplier on listening time (2.3), because the cap binds on time listened, which the files do not hold; kept in the world, reaching the golden through the past downgraders' own months, and no longer asked.
- 2026-11-12, architecture 5 at design: asks for what a downgrader brings and for the leavers' listening against their plan named the two valuations' intermediates and would have handed them over; both left inside R7.
- 2026-11-12, architecture 5's first cut (Flex 9.99 to 11.49, Gezin 22.99 to 26.49): returned by the holistic audit because the 2027 Gezin and Flex rises lay outside every past rise's size and overshoot, so whether the response grows with the rise was open and a dose-scaled reading withdrew Gezin (the platform run withdrew Flex and Gezin on log-dose scaling); the audit also showed the single-run truth check too noisy to test the golden (Flex's sign at EUR 0.50 a coin flip under replays). Repaired with each rise at its own past size, the rival's July 2026 rise and a replayed truth; Flex at 10.49 with the rival unmoved (truth EUR 0.04, se 0.3) was tried and rejected as a coin flip.
- 2026-11-13, the repaired cut (Flex 10.49, Gezin 23.99, the rival's July 2026 move, Onbeperkt alone going ahead): one trick by the author's audit and the new stump factorial; against the platform run's own route (downgraders kept, own listening) the crossing alone rescued four of five results. Re-designed with three stumps; persistence after a crossing rise (light listeners leaving from the third bill to the sixth) was tried as the second and dropped: it reached only Standaard, which the crossing already holds, so it never moved the call alone.
- 2026-11-13, stage 4 pass 1 on the factorial cut: the judge sent it back because the blocks did not say Gezin's December leaving was in the golden (it always was: +8.8 without it, +6.1 with it); the blocks now give every plan's December and listening rates and the leavers' valuation, and two readings joined the golden family (the plain mean of past crossings for a plan with none of its own; responses not floored at none), widening Standaard's and Gezin's first-bill bands. Pass 2 DETERMINISTIC, APPROVE.
- 2026-11-13, the reshipped cut (9ecc8c8, Gezin alone): returned by the platform's holistic audit (runs/arch5_audit_2026-11-13.md) on two counts, both true. Standaard's 2027 crossing had no past crossing of its own and the golden's carry was wrong against the world itself (21.2 and 16.1 per 100 against a replayed 4.5 to 7.4 and 41.5 to 43.9: the other plans' crossing downgrades were held down by profile limits that never bind on Standaard, and checks.py never set R3 and R4 against the replayed truth); and Onbeperkt's call turned on one constructed second-profile uplift that one table shows. The run pasted with it (runs/arch5_run2.md) made the crossing with the profile limit and the December leavers unprompted (R61, R62), so the factorial stood on the uplift alone. Re-designed in the same world at the audit's request: no 2027 configuration the record never ran, the uplift removed, the past e-mails dated, two processes the runs named and waved through (a stop followed by paying again, N33; the stayers' consumption response, N23) run on every plan; every graded figure now checked against the replayed world.
- 2026-11-13, a backtest of the 2026 rises predicted from 2025 alone as an ask (the audit's first example): Flex's and Onbeperkt's 2025 rises passed the rival and their 2026 rises did not, and Gezin's ran the other way, so a forecast from 2025 alone needs the cross-plan carry of a never-seen kind the audit refused for Standaard (the downgrades above all); its second example, a December effect under stated e-mail dates, is taken: the price list dates every past e-mail.
- 2026-11-13, Standaard's own past crossing (the rival's Plus 30 uur at EUR 14.49 in Flanders in 2025) to pin a 2027 crossing: pinned, but Standaard then held whatever the other judgments did; the rival's Plus 30 uur at EUR 16.99 keeps every Standaard rise below it, and Flex carries the crossing instead (its own 2025 Dutch rise, the rival's July 2026 rise to EUR 10.29).
- 2026-11-13, at design: the stayers' extra listening as one flat uplift on the whole account: it cost Flex and Standaard as much per hour as Onbeperkt and put every plan below zero; it falls on the account holder and grows with their listening, so it decides Onbeperkt and moves the others little.
- 2026-11-13, at design: Standaard's EUR 1.00 rise with the returns reached only EUR +0.1 in the replayed world, too thin to force; its past and 2027 rises are EUR 1.50, the 2027 rise still its own past rise in euros.
- 2026-11-13, at build: the stayers measured as accounts paying in December and in the month read (not in every month between) counted subscriptions that left and paid again by the summer; the stayers are those on the plan in every month to the one read.
- 2026-11-13, at build: the fade fitted across the plans puts Onbeperkt's 2027 extra hours at 37.8 against the replayed world's 26; the pack's own first-quarter months (18.9, 16.4, 17.8 per cent) support the fit, the plan-by-plan fade and the observed months sit inside the band, and no reading moves Onbeperkt off hold.
- 2026-11-13, stage 4 judge pass 3 on the first repaired cut: NOT_DETERMINISTIC, SEND_BACK. "Passes the rival" read two ways: crossing from at or below the rival's price (the golden) or a new price above it, and Onbeperkt and Gezin in Flanders had sat above the rival since their own 2025 and 2026 rises, so under the second reading their Flanders 2027 cells came from crossing events (10.8 to 29.7 per 100 against the golden's 0.9 and 0.6); only one past rise (Flex's Flemish 2026, already above) told the readings apart. Closed by construction, not by a sentence: the rival's Flemish Basis 10 uur at EUR 9.79 like the Dutch one (so Flex's Flemish 2026 rise crossed from below, as its Dutch 2025 rise did), and in July 2026 the rival's Basis raised to EUR 10.29 and its Flemish Onbeperkt and Familie brought to its Dutch prices, so no plan sits above the rival before any rise and both readings classify every case alike (SF20, asserted in checks.py and verify.py). The call holds (Standaard and Gezin).
- 2026-11-13, stage 4 judge pass 4 on the fixed cut: DETERMINISTIC, APPROVE (the rival comparison rebuilt region by region for every past rise and every 2027 cell, the October base reproduced; the returns and the stayers' listening components not rebuilt by the judge, carried by checks.py against eight replays of the world's 2027). Leak reader (run on the cut before the rival alignment, a data-only change): NO LEAK.
- 2026-11-13, re-root to architecture 6, stump screen on paper (stumping Part 3.4 and the full reflex list R01 to R83):
  in architecture 5's world only the stayers' listening is a stump runs lose (returns R76, the rival-conditioned
  transfer R77, the Flex one-region crossing R77, route migration one group-by and the listening's second channel, the
  catalogue addition the closed co-occurring-change card), so the world hosts one open member and is spent. A new
  B2B subscription world (the three segments with the lowest 2027 net revenue retention under a save-team cap) was
  screened and dropped before any code: expansion ramps slipping against contracted dates is a reflex (R65, R73),
  monthly overage on commits reset at renewal is a convexity runs simulate (R53), and renewals reset toward active
  seats is one join and one regression of the usage log against the contracts; its domain fit read as revenue
  operations. The open class with no reflex on file is source assignment (L03, N14, N27, L44, L08: a second
  instrument at another grain set aside), the approved builds' anatomy.
- 2026-11-13, architecture 6 screen, a second world prototyped and dropped (scratch, no task files): a mobile
  subscription app's 2027 acquisition in six channel and platform cells, each cell's 12-month net revenue per install
  against its quoted cost per install. Four of the six cells were forced, because each cell's value was read from one
  complete instrument (Apple Search Ads by Apple's own attribution, the three Android cells by the attribution export),
  so every route filed them alike. The two iOS ad-network cells were both opened by the one consent stump, one open
  member. And the golden failed on identifiability: the value-by-conversion-value map pooled over iOS users carried
  Apple Search Ads' engagement within each value, putting TikTok iOS at 5.27 against the truth's 4.53, while the
  shortcut that reads withheld values as zero landed at 4.24 (off 0.74 against 0.29).
- 2026-11-13, stage 4 on architecture 6's first cut (9db89e979fe735f2): the determinism judge (pass 5) returned
  NOT_DETERMINISTIC, SEND_BACK because the growth policy's section 3 rendered blank (its bands table was built with
  the column widths passed as a dictionary, so the export dropped it), and the isolated reader found the same blank
  section and three cutoff dates side by side (the accounts and spend extracts stopping on 1 November against a 9
  November pull, the policy's "records to the end of October"). Fixed in one pass: section 3 states the bands as a
  sentence and a correctly built table; the fork checks read the shipped PDF's own text (SF9 had read the source); the
  exports carry the installs of the pull week (2 to 8 November 2026) on a random stream of their own, so every
  extract runs to 8 November and no media week's draw moves; section 4 reads "records to the start of November"; two
  forks added (SF12 a charge's day, SF13 the incomplete pull week). Every band held; figures moved at the sampling
  level only.
- 2026-11-13, stage 4 judge pass 6 on the fixed cut (90e641dd3185f4cd): pass 5's blank section closed; a new
  FIX_NOW on the answer blocks only: AppLovin Android's R2 band (3.37 to 3.67, a 0.15 floor) and R3 band (6 per cent)
  each let a figure inside its band carry the return under 0.90 (0.8997 at R2's floor with R3's point). Fixed in the
  answer blocks: R2's and R3's bands are each capped per channel at the channel's margin to its nearest line over 2.2,
  so both at their edges together keep the band (AppLovin Android 2.1 per cent each, the honest family's spread 0.2
  and 0.4 per cent), asserted corner by corner in checks.py; the stores' excess, which the judge reproduced at 41.4 to
  41.6 per cent on another basis, is stated as about two fifths. No graded figure, prompt or pack moved (the cut is
  unchanged), so no further judge pass.

- 2026-11-16, architecture 6's first cut (READY 145d6ea, never uploaded): its asks were graded on inputs of their own
  (the installs each channel bought, the 2025 installs' value, installs a week at the plan's spend) and its careful pass
  was priced at 48.2; under the rule of 18a93a7 the run that missed the call would have collected them. Core redrawn in
  place and proved in generator/core.py before any file was touched.
- The spend response as the third stump (installs dearer and weaker as weekly spend rises, the first cut's J3): one plot
  of one file shows it and a fitted response curve is the runs' reflex; replaced by what a budget buys, the week's spend
  being the auction's outcome.
- Tracking consent gating the channel on Android too, the Android accounts with no channel split between four sources:
  the Play install referrer names every Android install in the real process, and a four-source mixture was not
  measured to the precision the lines need.
- A store-side count of buyers by acquisition channel as S1's second record: one join would hand over the charges the
  records lack channel by channel.
- The value response read on the named installs as a separate stump: it is S2 at another cell, and one sentence
  rescued both.
- The stores' commission stepping at a revenue threshold: a filed term, rule application.
- Store console downloads, ad revenue allocation, billing retry, account deletion, a 24-month window, audiences used up
  and paid installs taken from organic: hygiene the runs do unprompted, or the client's closed cards.
- Meta Android as a member: S2 is silent on it and the reflex route filed its band, a free band and free figures.
- Apple Search Ads as a member of the call: S2 is silent on a channel whose every install is named and the direct
  route's errors cancelled there; it runs on a fixed brand budget outside the plan and is S2's referee.
- One price for every unnamed install whatever its network (the accounts with no channel's own value by cell) as the
  golden: biased by channel (TikTok iOS 4.5 per cent high) and 5 times the golden's error on Apple Search Ads' unnamed
  installs (10.89 against 11.71, the golden 11.58); kept in the battery.
- Apple Search Ads' own ratio of unnamed to named value as the golden: it leaves the accounts with no channel 4 per cent
  short of what they paid (0.958); kept in the battery.
- The moved weeks as a referee against spend instrumented by the budget: the instrumented fit passes it (1.386 against
  1.363), so it and the budget alone are honest variants in the battery, never rivals.
- Google Android with more subscribers who go quiet than its store's average: the true-up then erred upward there,
  cancelled part of the spend response's error and the rigorous route filed its band; it now sits below its store's
  average.
- A break-even weekly spend per channel and an equal-marginal reallocation as ask families: their honest bands (the
  elasticities' spread carried through an inverse) swallowed two of the three stumps.
- Installs a week at the plan's spend and cost per subscriber as ask families: free to a run that lost S1 or S2.
- A daily grain for the response: a daily fit summed to weeks loses the bias as fast as the instrument gains precision,
  and the team sets budgets by the week.
- The iOS networks' unrecorded share and Google Android's installs a week as components: with them S1 owned no figure
  the route that loses the other two stumps lands (corelib: no figure of its own); the four components are AppLovin
  Android's unrecorded share, Meta iOS's value per install, what the stretch spend adds and the iOS networks' plan
  revenue.
- The delivery share at plus and minus 20 per cent in the forcing block (the build, 2026-11-16): it is a ratio of two
  recorded totals, and 20 per cent down carries Meta iOS (1.21) and AppLovin Android (1.20) over the scale line; it is
  run at 9.6 per cent each way, the widest departure of any channel's quarter from its 104-week share, and the note's
  Forcing line says so.
- A card settlement report by charge month: a processor pays out two banking cut-offs on, so the report is by payout
  month and stops at the pull; it reconciles the web checkout's charges in total and decides nothing.
- No two days of total ad spend equal as a realism assertion: across 728 days of totals near EUR 6,000 two pairs agree
  to the cent by chance; the assertion is that no channel spends the same amount in two weeks and no day's rows repeat.
- 2026-11-16, architecture 6, stage 4: bands set as the range of 26 variants widened a quarter each side. The judge's
  literal rebuild of the steps (the equations carried as fitted, value on the complete weeks' own values, seven
  channels in the month pattern) landed Google Android outside three of its four bands; the battery now carries that
  reading in 15 forms and 22 crosses (71 variants) and the bands are their range with a tenth each side.
- 2026-11-16: a week's month from its Monday, the equations in levels or in levels on the logs, one price ratio for
  all first-48-hour values and the annual trials left out, kept in the bands. With them in, the next-euro bands
  widened until a run that lost the stores' excess landed inside most of them, and the spend fit's move on Google
  Android (0.184) fell to 2.8 times the variants' spread there (a variant at 0.969); each is refuted by a figure from the shipped files
  (the plan's blocks, the moved weeks, Apple Search Ads' unnamed installs, the stores' annual first charges), so they
  are run, reported and kept out.
- 2026-11-16: the attribution export's install time written 40 to 640 seconds after the account's creation. Read as
  the install clock, the judge found, it dropped 1,349 charges made between the two times; an app's first open precedes the sign-up, and
  the export now writes it that way (a minute or so before on most accounts), so both clocks file the same figures.
- 2026-11-16: the conversion-value file named `skan_conversion_schema.json`, then with a `_v3` suffix: the first name
  says it describes the data and the second reads as a working copy; it is `skadnetwork_conversion_values.json`.
- 2026-11-16: the change log's notes drawn from eighteen fixed phrases with one closing phrase on every return to
  base: the reader marked it as generated; the notes are now composed from the quarter, the month and the weeks, about
  a third of the rows are left empty and a return to base closes five ways.
- Stage 4, the judge's second pass: the first widening of the battery (every listed way under each as-fitted carry,
  195 variants then with Apple Search Ads' ratio as one number among them) kept the rule of a tenth of the range each
  side, and on the wider ranges that pad alone took the true-up's and the spend fit's routes inside eight more bands
  (a run losing only S1 earned 45.5 and only S3 48.6). Dropped for half a per cent of the figure each side, the size
  two rebuilds of one variant differ by: 40.5 and 39.8.
- Apple Search Ads' ratio as one number sat in the battery for one run of the gates: it set the upper edge of the iOS
  plan revenue (1,253,000) and with it the spend fit's route earned Component 3 (S3 lost alone 46.7). It is a single
  ratio across first-48-hour values, which its own trial starters refute by session bucket (18.95 against 16.50 paid,
  29.31 against 32.24), so it went to the refuted readings beside the other single ratio (SF30) and the battery keeps
  the ratio by two groups and value by value.
- A band with no allowance beside the battery's range (S1 36.7, S3 36.0): not taken, because the judge's own rebuild
  of the golden differs from ours by up to 0.01 on a return, and a band cut at the battery's last digit would call an
  honest rebuild of an edge variant a miss.
- Architecture 6's second step as the deciding lesson (one ratio for every source, fitted so that the accounts with no
  channel add up): redrawn on 2026-11-21 under the client's phase 2 bar, before any upload. Read by its fix it is a
  gross-up from an independent total, the completeness card's remedy, and its lesson key was closed by the page's read
  of 2026-11-21. In the redrawn world, where a declined install's worth differs by network, it is a priced shortcut
  (Meta iOS 1.38, scale; 45 on the rubric).
- Architecture 6's first step as it was graded (one continuation for every subscription nobody opens, its component
  the share of revenue the records never took in): the web checkout's continuation read off the records gave the same
  figure, which is a factor handed over by checked cases, and the component named the correction. The world now
  separates three continuations (0.97 a month on a store, 0.91 while the app still sees the subscriber, 0.88 on the
  web checkout) and the step's own figure is what an install went on to pay.
- Architecture 6's component block (the unrecorded share, the adding-up ratio and two figures that fell with two or
  three stumps): two stumps owned no component, so a run that lost one step could not earn the others'. One component
  per stump now, each asked for in the decision's words, and four asks in place of the earlier list.
- A first cut of the redrawn first step in which the cancellations the app saw, or the web checkout's rate, completed
  the stores' excess well enough to leave AppLovin Android in hold: the two standard completions were an easier second
  route. The process was retuned (a subscriber who cancels while still opening the app is seen cancelled at a later
  open; a store subscription nobody opens lapses far more slowly than a web one) so that both file AppLovin Android in
  cut (0.881 and 0.847) and both take in only 56 to 68 per cent of the stores' renewal excess.
- Six other campaign calendars (CAL_SEED 7300 to 7350): over six draws of the people each identified one source's
  ratio or more less precisely (root mean square error up to 0.049, against 0.031 at most on 7360, the one kept).
- Channel placements that re-drew a channel's people whenever its plan moved: replaced by plan and stretch factors
  that are exact dials, so a channel is re-placed against its line without touching the record; two channels were then
  re-centred so that each call survives its fitted ratio moved a fifth either way (Meta iOS 0.945 and 1.156, Google
  iOS 1.255 and 1.646, Pinterest iOS 1.374 and 1.783).
- The groupings the fit cannot tell apart (Google iOS with Pinterest iOS at 2.87 against 3.84, either with the organic
  installs, all three at 3.01 against 5.99) left outside the battery: not taken. They are four of the 32 variants,
  they file the golden call and the ranges hold them; the groupings the fit refuses (the four social networks, 74.0 on
  three degrees of freedom) stay outside as refuted rivals, and the two pairs refused only narrowly (4.43 and 4.49
  against 3.84) file the golden call.
- The delivery share taken over the 104 weeks or the mature weeks only: the last 52 weeks is a defensible forecasting
  base (the judge of architecture 6's cut said so), so it joined the battery as the 32nd variant. The installs-a-week
  ranges widened, the response on spend now lands three of them (Snapchat iOS, Google iOS, AppLovin Android), and a
  run that loses S3 alone moved from 41 to 47, the reflex route from 12 to 16.
- AppLovin Android's plan factor at 0.92 (golden 0.955): with the delivery share moved up by its widest quarter (9.6
  per cent) its return came to 0.901 against the 0.90 line. Moved to 0.88 (golden 0.970, 0.916 under the same move).
  0.86 (golden 0.978) was tried and not taken: it brings the shortcut that carries the candidates at the cancellations
  the app saw to 0.888, too near the line it has to land under.
