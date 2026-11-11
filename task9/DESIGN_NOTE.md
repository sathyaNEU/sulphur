# task9: what is causing the edge-ring on Tessaline Fab 2's wafers, what it has cost since April, and when the part responsible should be replaced

## Draw

Subdomain: General Statistics & Data Science, Interpretability (feature attribution and mechanistic analysis: a sort-yield
  loss attributed across correlated process features to the part whose wear carries it); the author supplied the draw as
  Concept 2 of the three concepts prepared on 2026-11-10.
Analysis type: Root-Cause Analysis, ending in a dial setting
Answer shape: ranked causes with their contributions: the ring's loss since 1 April measured and split across its causes
  (conditioner-disk wear, pad life, the rivals at about zero), with the policy bridge and the disk-only change interval
  that follows.
Weight: attribution. Most of the work is splitting a measured loss across candidate features that move together: tools
  routed together, a scanner that arrived the same month, and three CMP counters (pad, disk, retaining ring) that reset
  together at a full preventive maintenance; the last three builds sat on investigation (task20), modeling (task21) and
  validation (task9's first architecture).
Data-native sentence: a fab's sort records see the ring only as zone fail counts on every wafer and as die bins on a
  sample the yield team pulls mostly from flagged wafers, its process records route one deposition chamber's lots to two
  of the four polish units, and its maintenance log resets the disk, the pad and the ring together except in a handful of
  free-text episodes, so the loss, its cause and its dose all have to be rebuilt from records that each see one face of it.
People: Katelyn Bailey (yield engineering lead), Victor Kelley (CMP module engineer), Leah Griffith (equipment
  maintenance lead), Elizabeth Sandoval (fab finance, owner of the cost inputs); drawn with guard.py names --geo us --seed 9021.

1. Fit: the client's direction is the yield-loss decomposition and tool-commonality literature named in the concept; the
   draw is not a reskin of any client task (skeleton.py check, nearest severity none).
2. Task type: regression and model diagnostics serves forecasting in the house mapping, so the root-cause analysis is drawn
   under Interpretability, the General Statistics task type that serves Root-Cause: feature attribution under dependence and
   a mechanistic dose-response are its own objects.
3. Data: generated, simulating the fab's process (lot starts and product mix, dispatch with one chamber-to-unit affinity,
   clustered random defects and a fab-wide particle week, the band's normal roll-off, conditioner-disk wear with a per-unit
   rate and a pad term, the maintenance timeline under Rev E, Rev F and waiver EW-118 with disk-only and ring-only swaps,
   edge removal-rate metrology, the fab's ring classifier, the yield team's die-map pulls).
4. Decision: the maintenance-spec change (Rev G) for the CMP conditioner disk, at the module team's review; backward on the
   loss, forward on the interval.
5. Shell: question form what; one deliverable, a short deck for the module team's review (pptx), away from the over-quota
   workbook sets and from every shell in the slot's lineage.
6. Card: shape 04, gap objective then population, generators G4 (attribution at a transition), G16, G6, Gate G
   decomposition_attribution, calibration form physical_verification (the edge removal-rate metrology), context artifact
   monitoring_export (the classifier's labels), forum line_manager_or_team, forcing event incident_or_complaint (the
   excursion ticket), organisation manufacturer, role field_unit_lead, strategy decomposition_attribution.
7. Guard: registered 2026-11-11, WARN only: repeat.gate_g (after task20, whose split is a forecast's misses), repeat.decision
   (dial_setting after task21's rate change), repeat.question_form (what), skeleton.house_lesson (the routing rival is a
   supporting step, never the deciding lesson).
8. Slot: architecture 1 of the cleared slot (Concept 1) is spent and in the card's lineage.

## Results chain

Sketch at the draw; pins, bands and the carry-forward line are written at stage 2.

| ID | Result (checkable) | Area | Hurried analyst |
|---|---|---|---|
| R1 | The ring's loss 1 April to 31 August in points of mean sort yield over every sorted wafer | missingness-measurement | dismissed own evidence: the classifier's EDGE_RING wafers only; first story: before and after April with the particle week and the mix shift inside; method shortcut: the die-map sample read as the fab |
| R2 | The same loss in good die by product | decomposition-attribution | method shortcut: the fab's points spread by wafer count, not by each product's band |
| R3 | The causes ranked with their shares of R1 | investigation-loops | first story: tool commonality stops at the CMP2 units with DEP-3 behind them, or at the new scanner |
| R4 | The onset in conditioner-disk usage and the slope after it | causal-reasoning | first story: the pad counter the FDC shows, or wafers since full PM |
| R5 | The retaining ring's and the pad's terms | modeling | unfinished chain: the full PM's parts never separated |
| R6 | The edge removal-rate check's onset in disk usage | self-verification | earned by careful runs |
| R7 | The loss split between Rev F's extension, the EW-118 reused disks and the old rule's own exposure | decomposition-attribution | first story: the whole loss put on Rev F |
| R8 | The disk-only change interval for each unit group and its annual saving | synthesis | method shortcut: one pooled interval, a full-PM lever, or a dose from zero |

## Tried and rejected

- 2026-11-11, missing data, censoring and measurement error as the task type: the taxonomy has it serve descriptive work,
  monitoring and comparison, not forecasting (guard three_rules.task_type), so the forecast is drawn as a posterior
  predictive count under Bayesian modeling and posterior inference.
- 2026-11-11, Concept 3 (the speech model under the speed cap): benchmarking and ablations is task15's task type and its
  lessons sit on the client's strategies 4 and 5; Concept 1 drawn first as the author's ranking puts it.
- 2026-11-11, the hot batch read from the simulator's own window (record.py carried params' build weeks): the golden
  cannot know a window the pack does not show, so the window is found from the record by a build-week scan of the last
  year's replacements against each vault's earlier level, with nothing flagged under a likelihood ratio of 25.
- 2026-11-11, batch frailty at gamma(12) (cv 0.29) with a single-window scan: one high-frailty build batch made only the
  late weeks of the window stand out (seed 9011 found weeks 25 to 30, and 16 to 32 once the vault levels were in), so
  batch frailty is gamma(30) (cv 0.18) and the scan takes each vault's own earlier level; seeds whose scan misses the
  true window were set aside.
- 2026-11-11, the infant term fitted on half-year age bands and applied to a drive's first weeks: the band-mid covariate
  inflated the term's coefficient to about 150 times at install and put the new X-24 vaults at three times a believable
  first-year rate; the first year is now fitted in monthly bands.
- 2026-11-11, Poisson or drive-level-draw bands as the careful pass's priced loss: frontier runs bootstrap and build
  predictive intervals unprompted (precedents R04), and with each vault's level in the golden the vault-quarter residuals
  carry no extra-Poisson spread, so the interval and the back-test are not priced on clustering; they stay as graded
  results the careful pass earns, and the band's width is graded with the path.
- 2026-11-11, the migrate call for the batch as a whole (migrate if the batch's 24-month share exceeds 20 per cent): every
  route that finds the batch at all lands on "migrate", so the call priced nothing; the call is made vault by vault, where
  a vault holding a third of the batch does not pay.
- 2026-11-11, seed 9014 for the per-vault call: its vault B17 sat at 236 against the 240 line, flipping under either ramp
  shape alone; seed 9017 is the world where every vault clears the line by 10 per cent or more under every rival.
- 2026-11-11, the build window a week wider as a golden-family rival: the week-15 builds fail at 1.2 per cent a year, under
  the family's normal 2 per cent, so the data rule the wider window out; it moves to the shortcuts (it migrates B15).
- 2026-11-11, the per-vault migration call as built on seed 9017 (stage 4 judge, NOT_DETERMINISTIC, SEND_BACK): the cost
  convention was open (the YAML's drive price and "new drives" licence break-evens of 130 and 678 beside the golden's 240),
  the prompt asked one call for "its vaults", the batch vaults' levels came from their few non-batch drives (B18 at 0.93
  against its record's 0.5, B16 at 0.84 against 1.56), and the batch's noisy quarterly rate (2.3, 3.9, 2.3, 6.1, 8.3, 7.8
  per cent) leaves a plateau reading that flips the call; the judge also found the build window at once, so R2 is not a
  loss a careful run makes, and with it earned the cited pair is near 58 to 65, over the bar.
- 2026-11-11, Concept 1 as a whole (Halden Vault's drive replacements): spent at stage 4 on the judge's SEND_BACK and an honest
  pair over the bar; the author chose Concept 2.
