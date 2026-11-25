# task7 determinism check (Holistic Audit v4, determinism mode), 2026-11-25

Cut seen: prompt.txt 2a3c8fa9c0a7b81781098cb845b6bb90, target.zip 2b51dbaa6cf9378071b1c00459488f8b,
submission.md fa3340310bb72cd94a957570f358973d; 21 input files; prompt not yet rewritten. No runs yet (Part B steps 3 and 5
on the runs wait for the holistic pass). Scripts: the judge workspace's `work/` (prep.py, steps.py, model.py, run.py,
study2.py, sustain.py).

**Verdict: DETERMINISTIC. Disposition: FIX_NOW** (answer-block edits only: three missing convention sentences and the
bands that have to take the rivals they leave open). The fund set (Kettle Ridge, Larkin round, reconnection within 14 km)
held in every one of the 45 variants I ran in code, except two readings that figures from the files rule out.

## Step 0
Golden present: yes. Inputs belong to the task: yes (Cottonwood Draw, Sunflower Basin, the six proposals, every file the
Step-by-Step names are in the pack).

## Part A: correctness

My method: active A/C switches on the register; reach is the distance to the nearest on-air transmitter of the switch's
own system (receiver field), taken each event day from the site register and the outage log, with Pruett from 31 July.
Bands are 8, 14 and 20 km. The replaced-unit list comes from rebates (old numbers mapped through `old_premise_no`) plus
central A/C or heat-pump permits (addresses normalised), dated after install. Steps are taken at the first transmit of each
group (SCADA UTC-5, duplicates dropped, runs of 3 or more held readings dropped) as the 5-minute mean after less the 5 before. The
model is step = K x index x sum over switches of R(band) x B(group) x W(replaced) x district term, fitted by nonlinear least
squares with K = 0.802. Appraisal is on the 2027 footing at 1.15.

| Figure | Mine | Author | Agree |
|---|---|---|---|
| Fund set | KR, Larkin, Rec 14 km | same | yes |
| Kettle Ridge kW / break-even | 240 / 185.2 | 250 (231-262) / 185 | yes |
| Halverson fill-in | 159 / 279.5 | 185 (150-207) / 280 | yes |
| Larkin round (n) | 547 (1,578) / 279.7 | 505 (451-572) / 280 | yes |
| Medora Flats round (n) | 297 (1,242) / 400.8 | 264 (208-324) / 401 | yes |
| Reconnection within 14 km (n) | 1,368 (3,267) / 508.6 | 1,402 (1,252-1,552) / 509 | yes |
| Outlying reconnection (n) | 216 (1,239) / 344.9 | 224 (195-253) / 345 | yes |
| CC1 fringe reception vs within 8 km | 0.149 | 17 (10-22) | yes |
| CC2 installed through 2015 still working | 0.645 | 67 (63-70) | yes |
| CC3 still wired after replacement | 0.335 | 32 (27-37) | yes |
| Bridge: not received / failed / not connected / delivered | 1,639 / 2,713 / 1,584 / 5,148 | 1,775 / 2,396 / 1,626 / 5,200 | yes (in bands) |
| Funded plan kW, USD a kW-year | 2,154, 39.8 | 2,157 (2,046-2,285), 39.7 | yes |
| Counts: switches, days, commands, steps, replaced list, potential | 11,923; 60; 476; 21,896; 4,506; 10,997 | same | yes |
| Records-as-they-stand route: Larkin, Rec 14, explained | 58.2, 260.3, 789 | 58, 260, 799 | yes |
| Study homes to fleet: kW per enrolled switch, fleet kW | 0.720 to 0.731; 9,981 at 0.728 | 0.728; 9,981 | yes |

Internal consistency: the break-evens are cost/88 exactly, the plan's cost of USD 85,675 checks, the bridge sums to 10,997, and the call follows from
the prompt's rule. The Step 7 validation gaps (0.053 etc.) were not computed: they are incidental. I did not reproduce the author's
"78 rebuilds" or the leave-one-out table one-for-one; I ran my own (below).

## Part B: determinism

**Committed call:** fund KR, Larkin and Rec 14 km. **Deciding steps:** own-system reach by day, batch delivery, the replaced-unit term.

**Pins for the decision points that can move the call:**
- Reach on the switch's own system vs. either system. The either-system reading flips the call: KR 1 kW, and Medora and outlying get funded. Pinned by
  the work plan 6.4 ("the nearest transmitter serving them"), the register's `receiver` field, and the plan's 6.3 ("carrying the same group
  addresses as the present VHF sites"). The data agree: SSE is 2.397M own-system vs 2.440M either-system on 21,896 steps.
- Value per kW. The prompt says "at the plan's value per kW", and the plan gives USD 88. The rival that adds the invoice's USD 4.10
  transmission (USD 104.4 a kW-year) leaves the same call.
- Index 1.15, the 2027 transmitter footing, and each proposal alone: all pinned by the plan 6.4. The 1.15 is the mean of the
  four invoices' indices, 1.14975.
- Study homes carried to the fleet. Refuted: over the trial they predict 243,073 kW of steps against 122,039 recorded.
- The instantaneous step vs. the sustained peak-hour shed. Load over 17:15-18:55 against the step model's predicted shed (two-way
  fixed effects) gives a coefficient of 1.02 to 1.08 (se 0.013), which leaves the call unchanged.
- Working-switch kW K (the responder rule). The call holds for K from 0.66 (Larkin's break-even) to about 0.90 (Medora's).
  Every reasonable responder rule lands at 0.72 to 0.85. Only a t>3 screen (223 of 380 homes, K 0.962) funds Medora, and it is not a
  reasonable reading.

**Forks run (45 variants; all file KR, Larkin, Rec 14 except where noted).** The figures listed are the ones that leave the
author's bands:

| Fork | Leaves band |
|---|---|
| K = 0.721 / 0.728 (every study home treated as working) | CC2 0.718 / 0.711; Larkin 396 / 409; not received 1,474 / 1,488; failed 1,759 / 1,841; plan 2,017 kW at USD 42.5 |
| K = 0.743 (covariate mixture on the study homes: 97% respond; the author's ~91% is rejected at LR p about 0.002) | not received 1,519; failed 2,018; Larkin 437; plan 2,045 kW |
| K = 0.783 / 0.813 (t>1 / t>1.5 responders) | failed 2,842 at 0.813 |
| K = 0.85 (t>2 responders) | CC2 0.609; Larkin 636; Medora 347; failed 3,278 |
| New switch delivers the study homes' per-enrolled 0.728 (newB 0.908) or AC-16's level (0.893) | Larkin 409 / 387; Medora 219 / 206; plan 2,017 / 1,995 kW, USD 42.5 / 42.9 |
| Bridge on the four 2026 CP afternoons' transmitter sets (Pruett off, Halverson VHF down 13 Jul, Medora Flats down 31 Aug) | not received 2,206 (delivered 4,857) |
| Step window 3 min | CC3 0.398; CC2 0.611; Larkin 613; Medora 329; Rec 14 km 1,201; failed 3,031 |
| Step window 1 / 2 min | 1 min: CC1 0.070, CC2 0.729, failed 1,468, Larkin 363; 2 min: CC3 0.410 (noise: SSE 11.9M / 6.0M vs 2.4M, and the minute profile is flat from 0 to 9 min) |
| Batch as two eras (through AC-10, later) | CC3 0.211; Larkin 429; Rec 14 km 1,752; outlying 275; refuted, F = 3.9 on 14 df (p < 0.001) |
| Outages ignored | CC2 0.608; Larkin 626; Medora 335; failed 3,063 (ignores a shipped log; not a defensible reading) |
| Within band, no flip | windows 4, 6, 8, 10 min; Pruett from 3 Aug; band edges 8/11/14/17/20/25 and 5/10/15/20/25 (fringe switch-weighted 0.164 / 0.156); no district term; WLS; trim 10%; first, second and odd halves of the days (CC3 0.408 / 0.265 on half samples); replaced list by paid date (4,494), finaled permits only (4,493), with mini-splits (4,587); index origin -0.06 / +0.1; CP days dropped; four batch eras; replaced term by era (0.294 / 0.414); held readings kept |
| Leave-outs (refit without reach / batch / replaced term) | sets {Larkin, Medora, Rec14, RecOut} / {KR, Rec14, RecOut} / {KR, Larkin, Medora}; each raises SSE (2.409M to 2.532M) |

**Anomalies:** SCADA has 41,400 exact duplicate rows, which are dropped. Held readings do not change the result. The Pruett points are renamed 14 July and mapped through the point list.
No switching-log transfer falls on an event afternoon. The Halverson VHF outage is double-logged and both entries cover the same days. No
premise has two active A/C switches.

**Giveaways:** none. No file states the call, the shares or a proposal's kW.

**determinism: pinned** for the call. **unpinned_forks** (graded figures only, call unchanged):
1. **What a working switch takes off (K).** The Step-by-Step says "the 380 study homes' responders" but never says how a
   responder is classed. The defensible rules give K from 0.72 to 0.85, and CC2 and Supplementary 1c, 1d, 2a, 2b and 3 leave their bands (table).
2. **What a new switch delivers in a find-and-fix round.** The blocks credit a full 0.802. The author's own study homes are new
   2019-2020 switches and average 0.728 per enrolled switch. On that reading Larkin is 409 and Medora 219.
3. **Which transmitter set the bridge stands on.** "at the coincident-peak index" fixes the index but not the transmitters. The 2026 CP
   afternoons give not received 2,206.

## Fix (solution blocks only; nothing solvers see)

- **Step 2:** add the responder rule, i.e. how a study home is classed as responding, and say the bridge and the appraisal
  use the same K. If no rule in the pack forces 0.802, the bands below must take K from 0.728 to 0.85.
- **Step 8:** state what a replacement switch is credited with (a working switch at 0.802, or the study homes' per-enrolled 0.728).
- **Supplementary 2:** state the bridge's footing ("2027, every listed transmitter on the air, index 1.15") or widen not received to take 2,206.
- **Bands** (each wide enough for the rivals above; every break-even still clears by the same side):
  - CC2: 63-70 to 60-72.
  - Supplementary 1c Larkin: 451-572 to 385-640 (break-even 280).
  - Supplementary 1d Medora: 208-324 to 200-350 (break-even 401).
  - Supplementary 2a not received: 1,527-2,018 to 1,480-2,210.
  - Supplementary 2b failed: 2,056-2,823 to 1,750-3,300.
  - Supplementary 3: 2,046-2,285 kW to 1,990-2,330 kW, and USD 37.4-41.8 to 36.5-43.0.
  - CC3: 27-37 to 27-41 if the author keeps the 3-minute window among the conventions it accepts. Otherwise say in Step 1
    that windows under 4 minutes are dropped for noise, with the SSE figure above.
- **Optional, the author's call:** if the author would rather keep the current bands, the working level has to be pinned in the pack (for
  example a load research record of which study homes' switches were confirmed operating). That is a pack change and goes
  through `/fix-determinism`.
