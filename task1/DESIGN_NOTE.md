# task1: which band each paid channel of Zancada's 2027 media plan sits in

## Draw

Subdomain: Cohort and LTV modeling: retention curves, customer lifetime value (Product Analytics, retention-cohort-lifetime-value-modeling)
Analysis type: Forecasting & Predictive Modeling
Answer shape: a flagged set (each paid channel of the 2027 media plan placed in the growth policy's scale, hold or cut band, with the figures the band rests on: its return per euro at the plan's weekly spend and at the plan's stretch spend, the net revenue per install the plan's spend buys and what the next euro returns)
Weight: measurement: the work is measuring a return no record holds, each part of it from the record that sees it and each checked on a slice where it is known; none of the last three builds on file (task13, task16, task22) puts its work there
Data-native sentence: a store charge reaches Zancada's billing records only when the subscriber next opens the app, the attribution export names an iOS network only for the installs whose users allowed tracking, and a week's ad spend is what the platform delivered of that week's budget in that week's auction, so the twelve-month return of a euro of 2027 spend has to be estimated from the stores' reports, the networks' install postbacks, the accounts with no channel and the weeks the team moved a budget, each read for the part it sees.
People: Bernardo Pombo (head of financial planning, who signs the 2027 insertion orders), Magdalena Requena (head of growth, owner of the growth policy), Ester Rey (growth analyst, whose workbook the golden is), Rafa Naranjo (paid acquisition manager, who keeps the budget sheet) (`guard.py names --geo spain --seed 61113`). None appears in the prompt.

Architecture 6, core redrawn in place on 2026-11-16, before any upload (the cut of 2026-11-13 never went to the platform). That cut graded its asks on inputs of their own and priced its careful pass at 48.2; under the rule of 18a93a7 (every graded figure downstream of a stump, a run that loses one stump at 50 or under, the reflex route at 30 or under) the core was redesigned and proved in `generator/core.py` before any file was touched. The world and its people are kept. What moved: the plan's members are five iOS networks whose installs the attribution export holds only with tracking consent (Meta, TikTok, Snapchat, Google, Pinterest) and two Android channels (Google, AppLovin); Apple Search Ads runs on a fixed brand budget outside the plan and is in every record; the installs with no channel are priced so that they add up to what the accounts with no channel paid; the spend response of the first cut (a pattern one plot shows) is replaced by what a budget buys, the week's spend being the auction's outcome; and every ask is a figure the three estimates are used for.

## Stump screen

Screened on paper and in `generator/core.py --explore` before the card was re-registered (`references/stump-screen.md`, the seventeen tests).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A: a store charge reaches the billing records only at the subscriber's next open, and people who stop opening the app keep paying, more of them on some channels than others | the stores' excess over the records is spread like the recorded charges (N21, L44) | the stores' daily reports by product and event against the records' charges month by month, each account's last open and renewal setting, and the web checkout's subscribers, whose every charge is on file | none | kept |
| B: on iOS the attribution export names a network only where the user allowed tracking, those users are worth more than the rest at the same first two days, and the rest sit among the accounts with no channel | the installs the export names stand for the network's installs at the same first-48-hour value (L53, N27, L13) | the networks' install postbacks by value against the named installs, the accounts with no channel and what they paid, and Apple Search Ads, whose channel is on every account | none | kept |
| C: a week's spend is what the platform delivered of the week's budget in that week's auction, so weeks of high spend are weeks of cheap installs | the fitted response of installs to spend is what more spend buys (L51, L37, L28) | the team's weekly budget sheet beside the platforms' spend, and the weeks the team moved a budget | none | kept |
| D: a channel's installs come dearer and weaker as its weekly spend rises (the first cut's third stump) | 2026's return per euro holds at the plan's spend | weekly installs and value against weekly spend | 2 (one plot of one file shows it and the runs fit a response curve unprompted) | not a stump: it is the reflex inside C |
| E: tracking consent gating the channel on Android as well, the unattributed Android accounts split between four sources | the named installs stand for the channel | the Play console's acquisition counts | 8 and 11 (the Play install referrer names the channel on every Android install in the real process, and a four-source mixture is not measured at the precision the lines need) | dropped |
| F: the stores' commission stepping from 15 to 30 per cent past a revenue threshold | one commission rate | the stores' proceeds | 3 and 4 (a filed term applied; rule application) | dropped |
| G: paid installs taken from organic ones, and audiences used up as spend rises | the paid installs are additional | organic installs against paid weeks | 1 (the client's closed cards on displacement and on the easy cases used up first) | dropped |
| H: the 2026 installs not yet twelve months old completed from the older installs' later months | young installs read at their observed months | the 2025 installs' full twelve months | 1 (closed card: follow-up still open) | dropped: the twelve-month value is read on the 52 install weeks whose twelve months are on file |

## Deep reasoning

Task type: retention cohort lifetime value modeling (Cohort and LTV modeling: retention curves, customer lifetime value), which serves Forecasting
Domain test: every result is an acquisition-economics and lifetime-value quantity of a subscription app: the store charges the app's records never took in, an install's twelve-month net revenue where the attribution export names no channel, what a weekly budget buys in an ad auction, the return per euro at a plan's spend, the net revenue per install at that spend and the return on the next euro; it is the growth analyst's own lifetime-value and payback work.
Swap: "hold AppLovin because the stores go on charging the subscribers who stopped opening the app, hold Meta iOS because the installs the export cannot name are worth half the ones it can, hold Google Android because its cheap weeks were the auction's doing and not the budget's" makes no sense for a hospital or a grid: there is no store report beside an app's own billing sync, no tracking prompt, no install postback and no ad auction.
Where the weight sits: the twelve-month net revenue per install of every install each channel bought (R1 and R2): the stores' reports are set against the billing records month by month and the excess put on the subscriptions that were set to take it (a share of the trials last seen unconverted and a monthly continuation, both fitted to the excess), then each iOS network's installs the export does not name are counted from the postbacks by first-48-hour value and priced so that, with the organic ones, they add up to what the accounts with no channel paid; R3 to R6 carry that value through what a budget buys.
Layer 1: the attribution partner re-sends rows after an SDK retry and reports second devices as reinstalls; staff and test accounts carry sandbox charges; Apple reports its days in Pacific time and Google in UTC; a postback arrives three or four days after its install and carries no account; the networks' own install counts credit view-throughs; refunds sit in both the stores' reports and the records; the budget sheet rounds to ten euros and the platforms bill to the cent. None decides a band.
Not one thing: three stumps on three axes each open their own channel (## Stump factorial, ## Open members): the charges the records never took in (AppLovin Android), the installs the export cannot name (Meta iOS), what a budget buys (Google Android); a run that makes any two of the three still files one channel in the wrong band and earns 22 to 32 on the rubric, and a run that makes one earns 13 to 23.
One-fact test: the most useful sentence is the consent one ("the installs the export names are worth more than the rest at the same first two days, and the rest sit among the accounts with no channel"): on the reflex route it rescues no whole result and adds 13 rubric points (R6's first figure and four scattered figures of R4 and R5), and the pricing by cell, the adding-up constraint and the organic remainder are still to build; the stores' sentence rescues R1 alone (1 of 7 results, 5 points); the budget sentence rescues no whole result (2 points).
Not semantics: every field read as its system writes it still leaves each hurried result wrong: recorded_at says when the app took a charge in and last_open_at when the account last opened, and nothing says which charges are missing or whose they are; the tracking answer is a field on every account, and nothing says the consenting installs are worth more at the same first two days; the budget sheet and the spend export are two columns of euros, and nothing says which one the team controls in 2027.
Not rule application: the growth policy files the measure, the 365 days, the VAT, the commission and the fee, the marginal return and the lines; no filed procedure reconciles the stores' reports with the records, prices an install the export does not name or says what a budget buys.
Estimand: growth policy sections 2.1 to 2.6 (the return, an install, the twelve months, net revenue, prices and the trial, the marginal return), section 1 (the channels the policy places) and section 3 (the lines); the media plan's 52 weekly spends and its stretch spends; the prompt's populations (the installs each channel's 2027 plan spend buys), outcome (their twelve-month net revenue), window (the 365 days from each install) and units (euros per euro of spend; euros per install; euros per extra euro).
No decoy: no document argues a band; the networks' own install counts and the export's named installs are what those systems record, and no file carries a return per channel.
No replay: no result re-derives a published figure and no stated number is wrong.
Pinned: every graded figure is banded by the 19 variants of `generator/core.py` (five ways of fitting the charges the records never took in, six ways of pricing the installs the export does not name, eight ways of reading what a budget buys, among them spend instrumented by the budget and the budget alone); the call holds under every one; the rivals outside the bands are the three hurried choices, each refuted by its referee slice (## Stump core, Referee).
Run forecast: R1 lost to a method shortcut (the stores' excess spread over the recorded charges month by month, N21, L44); R2 and R6 to a method shortcut (every postback priced at the named installs' value, L13, N27, L53); R3 and R5 to a self-confirming check (the response fitted on spend passes its own hold-out, L51, L37, L28); R4 and R7 to dismissed own evidence on all three.
Strategy label: UNTESTED (record_algorithm_inversion, with linkage_missing_not_at_random and endogenous_supply_instrument)
Depth level: 5 by `generator/core.py` (CORE PASS level 5): three stumps on three axes, each necessary alone and none sufficient, three open channels each opened by its own stump, seven distinct wrong calls across the lattice and three among the single drops.
Lesson: a channel's twelve-month return is a quantity no record holds, and each part of it is estimated from the record that sees it and ruled on where it is known: the stores' reports for the charges the app never took in (put on the subscriptions set to take them, not spread over the recorded ones), the accounts with no channel for the installs the export cannot name (priced to add up to what those accounts paid), and the team's own budget moves for what a budget buys (the week's spend being the auction's outcome); no build on file teaches the three together.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the share of each channel's twelve-month net revenue (installs of 4 November 2024 to 2 November 2025) that the billing records never took in (AppLovin Android 0.348; from 0.136 on Google iOS) | missingness-measurement | policy 2.3 (every charge made in the 365 days); the stores' daily reports, the records' charges, each account's last open and renewal setting | AppLovin Android 0.347 to 0.354 | method shortcut: each recorded charge scaled by its store-month's ratio of charged to recorded, which puts 0.162 on AppLovin Android and 0.16 to 0.19 on every channel | independent: the stores' reports, the billing records and the accounts' last opens | Component 1 |
| R2 | each iOS network's twelve-month net revenue per install over every install it bought in those weeks (Meta iOS EUR 9.08) | missingness-measurement | policy 2.2 and 2.3; the install postbacks by first-48-hour value, the named installs, the accounts with no channel and what they paid | Meta iOS 8.77 to 9.36 | method shortcut: every postback priced at the value the named installs showed at the same first-48-hour value, which prices the accounts with no channel at 1.43 times what they paid | R1 | Component 2 |
| R3 | what a week's budget buys on each channel, and from it what one more euro on top of the plan's weekly spend returns (Meta iOS 0.57, Google Android 0.55, AppLovin Android 0.71) | causal-reasoning | policy 2.6; the budget sheet, the platforms' weekly spend, the installs and their value by install week | per channel, the 19 variants' range with a quarter of it each side (Google Android 0.50 to 0.57) | self-confirming check: installs and value fitted on the week's spend, whose hold-out error is small because the auction that moves spend moves installs with it; it files 32 to 73 per cent more per extra euro | R1, R2 | Ask 4 |
| R4 | each channel's 2027 return per euro at the plan's weekly spend, and the twelve-month net revenue per install of the installs that spend buys (Pinterest iOS 1.66 and EUR 10.93; Google iOS 1.43 and 9.87; Meta iOS 1.07 and 8.81; Google Android 1.04 and 9.72; AppLovin Android 1.03 and 5.27; Snapchat iOS 0.64 and 7.53; TikTok iOS 0.61 and 6.22) | forecasting | policy 2.1; R1 to R3 carried through the plan's 52 weeks | per channel (return: Meta iOS 1.04 to 1.11, Google Android 1.02 to 1.07, AppLovin Android 1.01 to 1.07) | dismissed own evidence: the true-up in proportion, the named installs' value and the response on spend together file Meta iOS 1.35, Google Android 0.80 and AppLovin Android 0.74 | R1, R2, R3 | Ask 1, Ask 3 |
| R5 | each channel's return per euro at the plan's stretch spend (Pinterest iOS 1.29, Google iOS 1.24, Meta iOS 0.95, Google Android 0.93, AppLovin Android 0.87, Snapchat iOS 0.61, TikTok iOS 0.58) | forecasting | the media plan's stretch spend; R1 to R3 | per channel (AppLovin Android 0.85 to 0.89) | self-confirming check: the response on spend, certified on held-out weeks, carries the plan's return almost unchanged to the stretch spend | R1, R2, R3 | Ask 2 |
| R6 | the twelve-month net revenue the plan's spend buys on the five iOS networks (EUR 1.22 million) and what the stretch spend adds across the seven channels (EUR 0.34 million) | decomposition-attribution | R4 and R5 summed over the plan's weeks | 1.18 to 1.24 million; 0.33 to 0.35 million | method shortcut: the named installs' value carried to every postback and the response on spend | R4, R5 | Component 3, Component 4 |
| R7 | each channel's band: scale Google iOS and Pinterest iOS; hold Meta iOS, Google Android and AppLovin Android; cut TikTok iOS and Snapchat iOS | synthesis | policy section 3 (cut under 0.90, hold from 0.90, scale from 1.20) | exact | dismissed own evidence: scales Meta iOS and cuts Google Android and AppLovin Android | R4 | Recommendation |

Carry-forward: every graded figure sits downstream of a stump and most of two or three. R1's AppLovin Android share falls with S1 alone and is S1's own figure; R2's Meta iOS value falls with S1 and S2; R3's next euro falls with S3 on every channel (Meta iOS's and Google Android's with S3 alone, S3's own figures), with S1 on three and with S2 on four; R4's returns fall with S1 on all seven, S2 on the five iOS networks and S3 on six, and its values per install with S1 on seven and S2 on five; R5 falls with S1 on seven, S2 on five and S3 on seven; R6's plan revenue of the iOS networks falls with S2 and S3 (S2's own figure of the components) and the stretch's addition with all three; R7 moves when any one stump is lost. Reflex work (the installs each channel bought, the recorded charges, the weekly spend) is done on every route and stated only in the Step-by-Step.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a subscriber who stops opening the app keeps paying, and the app takes a store charge into its records only at the next open | constructed, the process of client-side receipt sync and forgotten subscriptions | no: every channel, both stores and organic, from 12 per cent of Google iOS's twelve-month revenue to 35 per cent of AppLovin Android's | modelling: the stores' excess month by month against the charge dates of the subscriptions last seen set to renew | modelling (a share of trial-end candidates charged and a monthly continuation fitted to the excess, carried account by account) | keep |
| on iOS the attribution export names a network only where the user allowed tracking, and those users are worth more at the same first two days | constructed, the documented behaviour of the tracking prompt | no: every iOS network, organic and Apple Search Ads; 26 to 31 per cent of each source's installs consent and are worth about twice the rest | modelling: the postbacks by value less the named installs, set against the accounts with no channel and what they paid | modelling (the installs with no channel priced by cell so that they add up to those accounts' revenue) | keep |
| a platform spends more of a weekly budget in the weeks its auction is cheap | constructed, the delivery of a budgeted campaign in an auction | no: all eight channels in all 104 weeks | modelling: installs against the budget with the delivery beside it, checked on the weeks the team moved a budget | modelling (a response to the budget carried to the budget that delivers the plan's spend) | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the share of each channel's twelve-month net revenue the records never took in | Missed | Missed | Right |
| R2 each iOS network's twelve-month net revenue per install | Missed | Missed | Right |
| R3 what one more euro on top of the plan's weekly spend returns | Missed | Missed | Right |
| R4 each channel's return per euro and net revenue per install at the plan's weekly spend | Missed | Missed | Right |
| R5 each channel's return per euro at the plan's stretch spend | Missed | Missed | Right |
| R6 the iOS networks' plan revenue and what the stretch spend adds | Missed | Missed | Right |
| R7 each channel's band | Missed | Partly | Right |
| Roughly | 0 of 7 | 0.5 of 7 | 7 of 7 |

Measured by: generator/core.py on corelib.py at the draw (the rubric table of ## Stump core); .claude/skills/stumping/effort.py on generator/effort.json once the pack is cut
Largest single hint: the installs the attribution export names are worth more than the rest at the same first two days, and the rest sit among the accounts with no channel; rescues 0 of 7 results whole (13 rubric points through scattered figures); the stores' sentence rescues 1 of 7 results
Pair estimate: 11 (the reflex route on the rubric, from generator/core.py: 9 of it instruction-following; it lands one figure of 32, the next euro on AppLovin Android, and four of seven bands)

## Stump core

From `python3 task1/generator/core.py` (seed 71116, 713,534 accounts), every figure as printed.

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| AppLovin Android | 0.9/1.2 | 1.034 | 0.0247 | 0.7415 | 0.5982 | 0.7415 | S1 |
| Google Android | 0.9/1.2 | 1.035 | 0.0279 | 0.8011 | 0.6149 | 0.8011 | S3 |
| Google iOS | 0.9/1.2 | 1.428 | 0.0341 | 2.036 | 0.578 | 2.036 | forced |
| Meta iOS | 0.9/1.2 | 1.074 | 0.0239 | 1.346 | 0.4205 | 1.346 | S2 |
| Pinterest iOS | 0.9/1.2 | 1.661 | 0.0487 | 1.986 | 0.562 | 1.986 | forced |
| Snapchat iOS | 0.9/1.2 | 0.6405 | 0.0144 | 0.7938 | 0.2507 | 0.7938 | forced |
| TikTok iOS | 0.9/1.2 | 0.6128 | 0.0273 | 0.7742 | 0.2166 | 0.7742 | forced |

| Figure | Block | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|
| return Meta iOS | asks | 1.074 | 1.039 to 1.107 | moves | flips | moves | lost |
| return TikTok iOS | asks | 0.6128 | 0.5967 to 0.6488 | moves | moves | - | lost |
| return Snapchat iOS | asks | 0.6405 | 0.62 to 0.6619 | moves | moves | moves | lost |
| return Google iOS | asks | 1.428 | 1.381 to 1.459 | moves | moves | moves | lost |
| return Pinterest iOS | asks | 1.661 | 1.598 to 1.684 | moves | moves | moves | lost |
| return Google Android | asks | 1.035 | 1.02 to 1.071 | moves | - | flips | lost |
| return AppLovin Android | asks | 1.034 | 1.009 to 1.068 | flips | - | moves | lost |
| stretch return Meta iOS | asks | 0.9491 | 0.918 to 0.9864 | moves | moves | moves | lost |
| stretch return TikTok iOS | asks | 0.5785 | 0.5635 to 0.6127 | moves | moves | moves | lost |
| stretch return Snapchat iOS | asks | 0.6067 | 0.5872 to 0.627 | moves | moves | moves | lost |
| stretch return Google iOS | asks | 1.241 | 1.188 to 1.27 | moves | moves | moves | lost |
| stretch return Pinterest iOS | asks | 1.294 | 1.253 to 1.32 | moves | moves | moves | lost |
| stretch return Google Android | asks | 0.9318 | 0.9242 to 0.9507 | moves | - | moves | lost |
| stretch return AppLovin Android | asks | 0.8653 | 0.8451 to 0.8941 | moves | - | moves | lost |
| value at plan Meta iOS | asks | 8.812 | 8.522 to 9.084 | moves | moves | - | lost |
| value at plan TikTok iOS | asks | 6.223 | 6.059 to 6.589 | moves | moves | - | lost |
| value at plan Snapchat iOS | asks | 7.527 | 7.323 to 7.77 | moves | moves | - | lost |
| value at plan Google iOS | asks | 9.874 | 9.569 to 9.985 | moves | moves | - | lost |
| value at plan Pinterest iOS | asks | 10.93 | 10.52 to 11.04 | moves | moves | - | lost |
| value at plan Google Android | asks | 9.715 | 9.616 to 9.841 | moves | - | moves | lost |
| value at plan AppLovin Android | asks | 5.267 | 5.205 to 5.36 | moves | - | - | lost |
| next euro Meta iOS | asks | 0.5681 | 0.5238 to 0.6705 | - | - | moves | lost |
| next euro TikTok iOS | asks | 0.3605 | 0.349 to 0.398 | moves | moves | moves | lost |
| next euro Snapchat iOS | asks | 0.3918 | 0.3643 to 0.411 | moves | moves | moves | lost |
| next euro Google iOS | asks | 0.7588 | 0.6164 to 0.8259 | - | moves | moves | lost |
| next euro Pinterest iOS | asks | 0.9203 | 0.8758 to 1.033 | - | moves | moves | lost |
| next euro Google Android | asks | 0.5481 | 0.4978 to 0.5705 | - | - | moves | lost |
| next euro AppLovin Android | asks | 0.7052 | 0.6442 to 0.7641 | moves | - | moves | earned |
| unrecorded share AppLovin Android | components | 0.3484 | 0.3467 to 0.3541 | moves | - | - | lost |
| value per install Meta iOS | components | 9.079 | 8.772 to 9.359 | moves | moves | - | lost |
| stretch adds | components | 3.396e+05 | 3.323e+05 to 3.5e+05 | moves | moves | moves | lost |
| plan revenue iOS networks | components | 1.219e+06 | 1.183e+06 to 1.243e+06 | - | moves | moves | lost |

| Route | Call | Earns on the rubric |
|---|---|---|
| golden | right | 100 |
| S1 lost alone | wrong | 22 |
| S2 lost alone | wrong | 31 |
| S3 lost alone | wrong | 32 |
| S1 fixed alone | wrong | 16 |
| S2 fixed alone | wrong | 23 |
| S3 fixed alone | wrong | 13 |
| reflex route (every stump lost) | wrong | 11 |
| rigorous standard route | wrong | 11 |

CORE PASS level 5

Unobserved part: the twelve-month net revenue a euro of each channel's 2027 plan spend returns. No record holds three parts of it: the store charges made after a subscriber's last open (12 to 35 per cent of a channel's twelve-month revenue), the channel of an iOS install whose user did not allow tracking (about 72 per cent of each network's installs), and the installs a budget would have bought in a week whose auction was not the one that happened (the 2027 installs themselves do not exist yet).
Instruments: the billing records see every charge up to each account's last open and every web-checkout charge; read raw they file returns of 0.22 to 0.61 with the named installs (the direct route) and miss 12 to 35 per cent on the complete channels. The stores' daily reports see every store charge by product, event and country, with no account. The attribution export sees the channel of every Android install, of every Apple Search Ads install and of the iOS installs whose users allowed tracking; read as the channel it files Meta iOS at EUR 14.53 per install against 9.18. The install postbacks see every install of an iOS network with its first-48-hour value and no account. The accounts with no channel see what the unnamed installs paid, network and organic together. The budget sheet sees what the team set and the platforms' spend what was delivered; read as a response to spend they file an elasticity of 0.93 to 1.08 against 0.62 to 0.82.
Referee: three slices the plan's channels do not reach. S1: the web checkout's AppLovin Android subscribers, whose every charge the backend holds: net revenue charged after the last open per subscriber is 40.15, the golden's rule files 36.5 and the true-up in proportion 12.23 (7.7 times the golden's error; the one passed to corelib). S2: Apple Search Ads' installs whose users did not allow tracking, named by Apple's own attribution: EUR 11.71 per install, the golden's pricing 11.58, the named installs' value by first-48-hour value 16.18 and the named installs' mean 21.34. S3: Google Android's budget moves, each left out of the fit in turn: installs in the raised weeks over installs in the lowered weeks 1.363, the golden 1.406, the response on spend 1.823; spend instrumented by the budget (1.386) and the budget alone (1.383) pass with the golden and sit in the battery. Read raw as the answer the slices file nothing: the web checkout is 15 per cent of subscribers, Apple Search Ads is outside the plan, and the moved weeks are not the plan's.
Strongest standard route: AppLovin Android: the records trued up to the stores' reports month by month, the response fitted on spend with a hold-out, 0.7415 (cut); refuted by the web checkout's subscribers (12.23 against 40.15 after the last open). Meta iOS: every postback priced at the named installs' value by first-48-hour value on trued-up records, 1.346 (scale); refuted by the accounts with no channel, which that pricing puts at 1.43 times what they paid, and by Apple Search Ads' unnamed installs (16.18 against 11.71). Google Android: the same true-up and the response on spend, 0.8011 (cut); refuted by the moved weeks (1.823 against 1.363).
Said out loud: S1 "a store charge reaches the app's billing records only when the subscriber next opens the app, so the stores' excess belongs to subscriptions last seen still set to renew": four steps left (the candidates and their next charge dates, the share of trial-end candidates charged, the monthly continuation fitted to the excess, the charges carried account by account inside each install's 365 days). S2 "the export names an iOS network's installs only where the user allowed tracking, those users are worth more at the same first two days, and the rest sit among the accounts with no channel": four steps left (the unnamed installs counted by cell from the postbacks, the organic remainder, the ratio that makes them add up to those accounts' revenue, the cells too thin to price alone). S3 "a week's spend is what the platform delivered of the week's budget given that week's auction": three steps left (the response read on the budget with the delivery beside it, the fitted installs brought back to the history's total, the plan's spend carried at the budget that delivers it).
Worth: S1 0.227 on AppLovin Android, 9.2 times the family's spread of 0.0247. S2 0.256 on Meta iOS, 10.7 times 0.0239. S3 0.184 on Google Android, 6.6 times 0.0279. Each open member's margin to its nearest line (AppLovin Android 0.134, Meta iOS 0.126, Google Android 0.135) is about five times its family's spread and smaller than its stump's worth.
Regimes: second stump on every member: S1's rule is checked on the web checkout's subscribers of every channel and cannot be checked on a store subscriber; S2's pricing is checked on Apple Search Ads and on the adding-up of the accounts with no channel, and does not apply to Android (every install named); S3's response is checked on each channel's own moved weeks. S2 opens Meta iOS, S3 opens Google Android and S1 opens AppLovin Android.
Sharp: S1: its wrong route passes the control total (the trued-up records equal the stores' reports in every month); its right route commits to which subscriptions took the unseen charges and at what continuation; the evidence is in the web checkout's charges after the last open; the correction runs from 0.136 of Google iOS's revenue to 0.348 of AppLovin Android's while the true-up puts 0.16 to 0.19 everywhere; its own figure is AppLovin Android's unrecorded share. S2: its wrong route reconciles installs to the postbacks cell by cell; its right route commits to a price for installs no record names; the evidence is what the accounts with no channel paid and Apple Search Ads' unnamed installs; the correction lowers the five iOS networks by 18 to 21 per cent and leaves Android alone; its own figure among the components is the iOS networks' plan revenue. S3: its wrong route passes a hold-out of weeks and a back-test (the auction moves spend and installs together in held-out weeks too); its right route commits to the budget as what the team controls; the evidence is the moved weeks; the correction raises Google Android by 22 per cent and Pinterest iOS by 14 (the plan spends less there than the record did), lowers Meta, Snapchat and Google iOS by 4 to 5 (the plan spends more) and leaves TikTok iOS's return a near miss; its own figures are the next euro on Meta iOS and on Google Android.
Earns: a run that loses only S1 earns 22, only S2 31, only S3 32 (50 or under each); the reflex route earns 11 and the rigorous standard route 11 (30 and 50 or under); S1 fixed alone earns 16, S2 fixed alone 23, S3 fixed alone 13 (each more than 11 and a third at most). The reflex route still lands one figure, the next euro on AppLovin Android (its three errors cancel inside a band of 0.64 to 0.76): kept, because the ask is the same figure for every channel of the plan and dropping one channel's row would name it.

## Stump factorial

Reflex route: the installs of each iOS network counted from its postbacks and of the other channels from the channel on file; re-sent export rows, reinstalls, staff accounts and sandbox charges left out; net revenue at the policy's VAT, commission and fee; the twelve months read on the 52 install weeks that have them; the billing records trued up to the stores' reports month by month; every postback priced at the named installs' value by first-48-hour value; installs and value fitted on weekly spend with the month pattern and held-out weeks, carried to the plan's 52 weeks. It files Meta iOS 1.35 (scale), Google Android 0.80 (cut) and AppLovin Android 0.74 (cut) against three holds, with TikTok iOS 0.77 and Snapchat iOS 0.79 (cut), Google iOS 2.04 and Pinterest iOS 1.99 (scale): three bands wrong, 11 on the rubric.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 the stores' excess over the billing records belongs to the subscriptions last seen still set to renew whose owners stopped opening the app | stump | each recorded charge scaled by its store-month's ratio of charged to recorded | N21, L44 | AppLovin Android cut (0.81) | Meta iOS scale (1.40) and Google Android cut (0.85), two bands still wrong; rescues R1 | no: the candidates, the trial-end share and the continuation are fitted to the excess and carried account by account |
| S2 the installs the export does not name are worth less than the named ones at the same first two days and sit among the accounts with no channel | stump | every postback priced at the named installs' value by first-48-hour value | L53, N27, L13 | Meta iOS scale (1.33) | Google Android cut (0.80) and AppLovin Android cut (0.74), two bands still wrong; no result rescued whole | no: the unnamed installs counted by cell, the organic remainder, the adding-up ratio and the thin cells |
| S3 a week's spend is the auction's outcome, so what a budget buys is read on the budget with the delivery beside it | stump | installs and value fitted on weekly spend, certified on held-out weeks | L51, L37, L28 | Google Android cut (0.85) | Meta iOS scale (1.28) and AppLovin Android cut (0.81), two bands still wrong; no result rescued whole | no: the estimator, the return to the history's total and the budget that delivers the plan's spend |
| J4 each iOS network's installs counted from its install postbacks | reflex | - | R81 | same call | - | - |
| J5 re-sent rows, reinstalls, staff and test accounts and sandbox charges left out | reflex | - | R80 | same call | - | - |
| J6 net revenue at the policy's VAT, commission and fee, over the 365 days from the install | reflex | - | growth policy 2.3 and 2.4 | same call | - | - |
| J7 a response curve with a month pattern and held-out weeks fitted to the weekly record | reflex | - | R92 | same call | - | - |

Level: 5: three necessary stumps, none sufficient alone, the single drops on three distinct wrong calls and the seven shortcut routes of the lattice on seven.

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| AppLovin Android | 1.034, hold (0.134 above 0.90) | 0.0247 | 0.7415, cut (wrong) | 0.5982, cut (wrong) | S1 |
| Meta iOS | 1.074, hold (0.126 under 1.20) | 0.0239 | 1.346, scale (wrong) | 0.4205, cut (wrong) | S2 |
| Google Android | 1.035, hold (0.135 above 0.90) | 0.0279 | 0.8011, cut (wrong) | 0.6149, cut (wrong) | S3 |
| Google iOS | 1.428, scale (0.228 above 1.20) | 0.0341 | 2.036, scale (right) | 0.578, cut (wrong) | forced (the reflex route files its band; its figures are all wrong) |
| Pinterest iOS | 1.661, scale (0.461 above 1.20) | 0.0487 | 1.986, scale (right) | 0.562, cut (wrong) | forced (as Google iOS) |
| Snapchat iOS | 0.6405, cut (0.260 under 0.90) | 0.0144 | 0.7938, cut (right) | 0.2507, cut (right) | forced |
| TikTok iOS | 0.6128, cut (0.287 under 0.90) | 0.0273 | 0.7742, cut (right) | 0.2166, cut (right) | forced |

Direct route: the pack's most direct evidence read at face value is the billing records as they stand, the installs the export names and the last full year's revenue over its spend (`generator/core.py`, `route(O, "raw", "direct", "average")`): the records miss 12 to 35 per cent of each channel's revenue and the named installs are about 28 per cent of an iOS network's, so it files every channel under 0.90 (0.22 to 0.61) and cuts all seven, wrong on five.

## Data provenance

Source: generated by task1/generator from a simulated subscription business: installs bought week by week on eight paid channels and two organic sources under the team's weekly budgets and each week's auction, each person's engagement, reachability and readiness to stop opening an app they pay for, the first two days, the trial, the plan, the store or the web checkout, the monthly charges, the last open, the tracking answer, the networks' postbacks and both stores' reports, with the app's, the attribution partner's, the networks' and the stores' records written as those systems write them (`generator/core.py` is the process and the generator writes its arrays to files).
Behaves like the real thing: client-side receipt sync leaves store charges unrecorded for subscribers who stop opening the app (a known gap of apps without server notifications); forgotten subscriptions keep paying for months; about three in ten iOS users allow tracking and they are the more engaged; a privacy-preserving install postback carries a coarse early value and no user; a budgeted campaign spends less of its budget when the auction is dear; a larger budget reaches into wider and weaker inventory; the networks' own install counts run above the postbacks.
Genuine patterns: (1) seasonality: January installs come in larger numbers and less engaged, August smaller, and planned spend follows the season (2) scale: installs rise less than in proportion to a budget (elasticities 0.62 to 0.82) and a larger budget brings less engaged people (3) cohort decay: monthly charges thin month by month, faster for subscribers who still open the app and cancel than for those who have stopped opening it (4) the trial: most first charges come on the seventh day, and conversion rises with the first two days' use (5) auction weather: each channel's delivery share moves week to week with some persistence
Problems by process: the partner's SDK re-sends rows after a retry; reinstalls on second devices; staff and test accounts with sandbox charges; Apple's Pacific days against UTC; postbacks three or four days after the install; view-through credit in the networks' own counts; refunds in both the stores' reports and the records; the budget sheet rounded to ten euros
Breadth: twelve or more files; 713,534 accounts, about 0.9 million billing events, about 270,000 install postbacks, two stores' daily reports, 104 weeks of budgets and spend on eight channels, three storefronts, two documents and two or more distractors; ten sources of installs, 32 first-48-hour values and 25 months of store excess, so which slice rules on which estimate is itself work

## Template check

Chain signature: missingness-measurement, missingness-measurement, causal-reasoning, forecasting, forecasting, decomposition-attribution, synthesis
Question form: which (which band each channel sits in)
Nearest build: task6 and task7 also file flagged sets, on quantities hard to measure (task6 flags services over an error budget from sampled spans, task7 feeders from a trial); here channels are placed in three bands on a forecast return whose every part is estimated from a different record, the chain opens on two measurement results and runs through a causal one, and no build on file shares the chain

## Frontier check

Precedents: R1 careful Missed on L44 (the level read off detailed records instead of the complete summary source) and N21 (an unmeasured component placed across the system in proportion to the metered quantities); R2 and R6 Missed on L13 (population rates applied to a subset selected by a score), N27 (a second record at another grain set aside because it lacks unit identities) and L53 (the selection seen, the unlabelled majority never estimated); R3 and R5 Missed on L51 (the most rigorous standard design the pack affords, whose own placebo cannot see the difference), L37 (a factor certified by a held-out error that cannot see its bias) and L28 (the estimator certified with checks that cannot see the problem); R4 Missed and R7 Partly on N21 and N27 together.
Shallow path checks: the true-up reconciles the records to the stores' reports exactly in every month, so its control-total check passes; only the web checkout's subscribers, whose charges after the last open are on file, refute it (12.23 against 40.15 per subscriber on AppLovin Android). The named installs' pricing reconciles installs to the postbacks cell by cell and reproduces the named installs' revenue; only the accounts with no channel (priced at 1.43 times what they paid) and Apple Search Ads' unnamed installs (16.18 against 11.71) refute it. The response on spend passes a hold-out of weeks and a back-test of the last quarter, because the auction moves spend and installs together in held-out weeks too; only the weeks the team moved a budget, each left out of the fit, refute it (1.823 against 1.363 on Google Android).
Assumption made false: the stores' excess is spread like the recorded charges (false: it belongs to subscribers who stopped opening the app, who are from 12 to 35 per cent of a channel's revenue; tested by the web checkout's charges in the billing records); the named installs stand for the network at the same first-48-hour value (false: the answer to the tracking prompt goes with how reachable a person lets an app be, which the first two days do not show and which carries conversion and retention; tested by the accounts with no channel and by Apple Search Ads); the response of installs to spend is what more spend buys (false: spend is the platform's delivery of a budget in that week's auction; tested by the budget sheet's moved weeks).
Forcing: the lines are 0.90 and 1.20. The golden family's widest move on an open channel is 0.028 (Google Android) and the nearest golden to a line is Meta iOS, 0.126 under 1.20 (0.104 under its nearest variant), with every one of the 19 variants on the golden's side for all seven channels. The shortcuts land across a line: S1 lost puts AppLovin Android at 0.81, S2 lost Meta iOS at 1.33, S3 lost Google Android at 0.85, the reflex route 0.74, 1.35 and 0.80. Each fitted input moved by its measured spread (the continuation read on the web subscribers, the trial-end share with the last two months left out, the pricing ratio at Apple Search Ads' own, the delivery share from the first 52 weeks, the slopes from the last 78 weeks) is one of the 19 variants and the call holds; the build adds each input at plus and minus 20 per cent in `effort.json` forcing.
Noun swap: nearest on file by skeleton.py check: severity none against every card, the client's corpus and the slot's lineage (task22 arch 2 and task16 v4 share record_algorithm_inversion and one detection, with a different decision form, answer pattern and mechanisms); swapping either build's nouns in carries one lesson of three across and nothing else.
Closed strategies: the call turns on record_algorithm_inversion (the records are the output of a sync at each open; the nearest closed card, recent counts still filling in, differs in mechanism and fix: the missing charges never arrive however long one waits and no completion factor by age recovers them, the fix assigns the stores' excess to the subscriptions set to take it), on linkage_missing_not_at_random (nearest closed card, self-selection into exposure: there is no treatment and no unit to compare with itself; the fix prices the unnamed installs to a control total at another grain) and on endogenous_supply_instrument (nearest closed card, a noisy explanatory variable flattens the slope: here the slope is steepened by a regressor the outcome's own process sets, and the fix is the team's budget as the instrument). No closed lesson is kept even as a supporting step: the twelve-month value is read on install weeks whose twelve months are on file, so no young cohort is completed.

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
| SF13 | the weeks the response is read on | the 104 weeks to 1 November 2026; without the launch quarter; the last 78 weeks | the 104 weeks | same call (two of the 19 variants) |
| SF14 | the budget that delivers the plan's spend | the plan's spend over the delivery share of all 104 weeks; of the first 52 | all 104 weeks | same call (one of the 19 variants) |
| SF15 | an iOS account with no channel | organic; an install nobody could name | an install nobody could name | the export gives the organic label only to accounts that allowed tracking, and each network's postbacks outnumber its named installs by more than three to one |
| SF16 | a postback's install week | its arrival day; its arrival less the schema's timer | arrival less three days | skan_conversion_schema.json (a 48-hour measurement window and a postback 24 to 48 hours after it closes); same call with four days (no channel's return moves by more than 1.1 per cent) |
| SF17 | the first-48-hour value's cells | the 32 values; eight or four groups; cells of 50 or more | the 32 values, cells under 20 through the source's tilt | same call (four of the 19 variants) |
| SF18 | the installs whose twelve months are read | installs of 4 November 2024 to 2 November 2025; every install with its months so far | the 52 weeks with twelve months on file | growth policy 2.3 (the 365 days); later weeks are valued through their first-48-hour values |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| VAT by storefront | 21, 22, 23 per cent | growth_policy_paid_channels_v3_2026-09.pdf, 2.4 |
| the stores' commission and the web checkout's fee | 15 and 3 per cent | growth_policy_paid_channels_v3_2026-09.pdf, 2.4 |
| prices and the trial | EUR 9.99 monthly, EUR 59.99 annual, seven days | growth_policy_paid_channels_v3_2026-09.pdf, 2.5; the billing events' own prices in billing_events_2024-11-04_2026-11-08.csv |
| the lines | 0.90, 1.20 | growth_policy_paid_channels_v3_2026-09.pdf, section 3 |
| the plan's weekly spend and stretch spend | 52 weeks by channel | media_plan_2027.xlsx |
| the first-48-hour value and the postback's timer | 32 values; 48 hours, then 24 to 48 hours | skan_conversion_schema.json |
| the billing cadence | a month of 30.4375 days | measured on the billing events in billing_events_2024-11-04_2026-11-08.csv; spread with a 30-day cadence in the battery |
| the share of trial-end candidates the stores charged | 0.087 and 0.088 monthly, 0.105 and 0.108 annual (Google Play, App Store) | fitted to the stores' first-charge excess in the two store reports (.csv); measured spread across one fit for both stores and the last two months left out |
| the monthly continuation of a subscription the app no longer sees | 0.888 | fitted to the stores' renewal excess in the two store reports (.csv); measured spread across two rates, a 30-day cadence, the last two months left out and the web checkout's own 0.892 |
| the price of an unnamed install by cell | the named installs' value times the ratio that adds up | accounts_2026-11-09.csv, skan_postbacks_2024-11-04_2026-11-08.csv and the billing events; measured spread across eight and four groups, cells of 50, one tilt per source, one price for all sources and Apple Search Ads' own ratio |
| each channel's budget and delivery slopes, the month pattern | fitted | budget_sheet_2024-2026.xlsx and ad_spend_daily_2024-11-04_2026-11-08.csv with the installs; measured spread across each channel's own month pattern, the launch quarter left out, the last 78 weeks, one value slope, spend instrumented by the budget and the budget alone |
| the delivery share that turns the plan's spend into a budget | each channel's spend over its budget, 104 weeks | budget_sheet_2024-2026.xlsx and ad_spend_daily_2024-11-04_2026-11-08.csv; measured spread with the first 52 weeks |

Variant battery: 19 variants beside the golden in `generator/core.py` (one fit across both stores, a two-rate continuation, the fit without the last two months, a thirty-day cadence, the continuation read on the web subscribers; cells in eight groups, in four groups, cells of fifty or more, one tilt per source, one price for every unnamed install, Apple Search Ads' ratio; each channel's own month pattern, the launch quarter left out, the value response on the mature weeks' own values, one value slope across channels, the delivery share from the mature weeks, the last 78 weeks, spend instrumented by the budget, the budget alone); every variant files the same call on all seven channels, and each graded figure's band is their range with a quarter of it each side.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the installs each plan channel's 2027 spend buys (R3 to R7); the installs each channel bought from 4 November 2024 to 2 November 2025 (R1, R2) |
| 2 | Unit of account: euros of twelve-month net revenue per euro of spend; euros per install; euros per extra euro; a share of revenue |
| 3 | Attribution window: the 365 days from each install's day |
| 4 | As-of dating: the exports pulled 9 November 2026, data to 8 November 2026 |
| 5 | Version basis: growth policy version 3 of September 2026; the media plan's draft of 30 October 2026 |
| 6 | Denominator: spend as the platforms bill it; installs as policy 2.2 defines them |
| 7 | Weighting: the plan's weeks weighted by their own spend and installs, nothing else |
| 8 | Window length: twelve months per install; 104 weeks of budgets and spend; 52 plan weeks from 4 January 2027 |
| 9 | Boundary inclusivity: an install on 2 November 2025 is in the mature year; a charge on day 365 is out |
| 10 | Rounding path: every figure at full precision to the end; returns stated to two decimals and euros per install to the cent in the answer blocks, each with its band |
| 11 | Tie-break: none needed; the nearest channel to a line under any variant is Meta iOS at 0.104 under 1.20 |
| 12 | Maturity and censoring: the mature year's twelve months are complete by 8 November 2026; later weeks enter through their first-48-hour values only |
| 13 | Order of operations: installs by channel, the charges the records never took in, the unnamed installs' price, the response to the budget, the plan and stretch spends, the bands |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: a re-sent export row (same install id) counted once; a reinstall is not an install |
| 16 | Identity normalisation: one account id across the accounts, the billing events and the export; postbacks carry none |
| 17 | Netting against gross: refunds netted; VAT, commission and fee taken off |
| 18 | Dimensional units: euros, VAT included in the price charged; weeks Monday to Sunday |
| 19 | Code and status semantics: production charges only; consumer accounts only; the first-48-hour value as the schema file maps it |
| 20 | Integerisation: none; installs a week stay fractional in the forecast |
| 21 | Clause scope: the bands apply to the 2027 plan's growth channels |
| 22 | Forward window contents: the media plan's 52 weekly spends and stretch spends; prices unchanged (policy 2.5) |

## Literal reader

Executing the shipped sentences word for word: policy 2.1 makes a channel's return the twelve-month net revenue of the installs a period's spend buys, per euro of that spend; 2.2 makes an install a new consumer account's first install, bought by at most one channel whether or not the partner can name it; 2.3 counts every charge the stores or the checkout made in the 365 days from the install, at its transaction time, net of refunds; 2.4 takes off VAT by storefront, the stores' 15 per cent and the checkout's 3 per cent; 2.5 files the prices and the seven-day trial; 2.6 makes the marginal return the twelve-month net revenue an additional euro of spend returns at a stated spend, every week raised in the same proportion; section 1 places the channels of the plan's growth sheet; section 3 cuts under 0.90, holds from 0.90 and scales from 1.20. The media plan gives each growth channel 52 weekly spends and stretch spends. Executed literally these fix what every figure is; none says how the charges the records lack, the installs the export does not name or the installs a budget buys are to be estimated.

## Prompt contract

A voice rewrite may not drop or change: the question (which band each paid channel of the 2027 media plan sits in under the growth policy), the plan's weekly spend as the basis, why the answer must be an estimate (the installs are not twelve months old until 2028; the records end 8 November 2026), the four figures for every channel with their units (the return in euros of 12-month net revenue per euro of spend at the plan's spend and at its stretch spend, the 12-month net revenue per install of the installs the plan's spend buys, what one more euro on top of the plan's weekly spend returns), "a committed figure for every channel", and the two deliverables by type (a workbook with the bands on its first sheet, the channel figures as a CSV). It must never add: a method, a comparison or an adjustment, a file name, a role, a rounding rule, a count of channels, or any word about tracking, the stores' reports, budgets or auctions.

## Build brief

World: Zancada Fitness S.L., a Spanish home-workout subscription app sold in Spain, Italy and Portugal (EUR 9.99 monthly, EUR 59.99 annual, a seven-day trial), 104 install weeks from Monday 4 November 2024 to 1 November 2026 and exports pulled 9 November 2026. `generator/core.py` is the process: the generator calls `core.simulate()` with SEED 71116 and writes its arrays as the systems would (the app backend's accounts and billing events, the attribution partner's export, the networks' install postbacks, the App Store's and Google Play's daily reports, the ad platforms' daily spend, the growth team's budget sheet and the 2027 media plan), then lays the Layer 1 mess on the files without touching an array the core reads.
Frozen: everything in `generator/core.py`: SEED, the dials of CH and ORGANIC (the members, their budgets, plan and stretch factors), CONSENT, CONV, DORMANT0, DORMANT, CHURN, CHURN_SILENT, the delivery constants, LINES, the golden estimators (`s1_values`, `s2_cells`, `ios_price`, `response`, `at_plan`), HURRIED, the 19 VARIANTS, the three referees, FAMILIES and COMPONENTS (the 28 ask figures and the four components). The build's analysis reads the files back into the arrays `Obs` holds and must reproduce the core's figures; a gate that cannot pass inside these comes back to the draw.
Files: accounts (one row per account: creation time, platform, storefront, the tracking answer, the first-48-hour value, billing route, plan and renewal setting as last seen, trial state as last seen, last open; never the person's traits, the wide inventory or the source of an unnamed install); billing events (every charge the app has on record with its transaction and recording times, store charges up to each account's last open and every web-checkout charge: the web checkout's subscribers are S1's referee and ship whole); the attribution export (install rows with the channel where the partner could name it: every Android install, every Apple Search Ads install, iOS installs whose users allowed tracking, the organic label only on accounts that allowed tracking; Apple Search Ads' installs whose users did not allow tracking, which the export still names, are S2's referee and ship whole); install postbacks (one row per install of the five iOS networks: arrival date, network, first-48-hour value, no account); the two stores' daily reports (units and proceeds by product, event and storefront, no account); daily ad spend by channel (spend, impressions, clicks, the network's own install count); the budget sheet (the weekly budget the team set per channel with its notes on each move, the moved weeks being S3's referee); the media plan (52 weekly spends and stretch spends for the seven growth channels, the fixed brand budget on its own sheet); the growth policy (PDF from a word processor); the conversion-value schema (JSON); two or more unlabelled distractors. Two CSVs of 20,000 rows or more. No file carries a return, a value per install or a ranking of channels.
Never filed: that a store charge is recorded "only when the app is next opened" or "at the next sync"; "dormant", "silent" or "forgotten" subscribers; that users who allow tracking "are worth more", "are more engaged" or "do not represent" the rest; "unattributed installs include paid installs"; "delivery", "pacing", "underspend" or "the auction" as a reason spend differs from budget; "budget is what we control"; any column named for a stump (no dormant flag, no wide-inventory flag, no auction index, no true channel on an unnamed install); any sentence telling which record to trust for what; file names that name a problem.
Goldens: `paid_channels_2027.xlsx` (first sheet: each channel's band with its return at the plan's spend and at the stretch spend, the net revenue per install at the plan's spend and what the next euro returns, and a chart of the returns against the two lines; behind it the unrecorded charges by channel, the unnamed installs' pricing and its adding-up, the response to the budget with the moved-weeks check, and a routes sheet setting the three hurried choices beside the estimates) and `paid_channels_2027.csv` (one row per channel: the four asked figures and the band). Every figure from `generator/figures.json`; the four components and the Step-by-Step counts in `submission.md`.
Free: file names and column names beyond the words above, the campaigns and creatives under each channel, the Layer 1 mess and its sizes, the distractors, the policy's wording outside sections 1 to 3, the budget sheet's notes (reasons a team gives for moving a budget, never the auction), the workbook's layout behind its first sheet.

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
