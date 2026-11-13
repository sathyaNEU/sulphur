# task24: which of the five Q1 2027 annotation requests Pellucid Annotation accepts at the clients' offered prices

## Draw

Subdomain: General Statistics & Data Science (Regression, classification & model diagnostics)
Analysis type: Forecasting & Predictive Modeling
Answer shape: forecast-bands-drivers: each request's expected fully loaded cost per delivered image (or frame) with
  its 80 per cent range and its drivers (review passes, floor top-up, annotator minutes), with the accept set and the
  price each declined request would need on top
Weight: modeling: the cost of each request is three modelling builds (an any-miss QA chain over each image's objects,
  each annotator-week's piece pay against the hourly floor, video frame time on track turnover); the last three
  builds sat in assembly (task13), a hard-to-measure quantity (task20) and synthesis (task23)
Data-native sentence: every 2026 cost the vendor paid is recorded at the grain of its own system (a task pass, a QA
  review, a worker-day punch, a worker-week pay line, an object or a track), so the cost of a request whose images are
  far denser, whose work is slower or whose video turns over more slowly than any 2026 project can only be built from
  the grain where each cost is decided
People: Loice Mumo (finance lead, owns the pricing policy), Collins Mutuku (QA lead, owns the review rubric), Jeffrey
  Reyes (Iloilo centre manager, timesheet notes); drawn with guard.py names (en_KE seed 2411, en_PH seed 2412)

## Stump screen

Written at the draw on 2026-11-13, before the card was registered and before any code. Each candidate went through
the nine tests of `references/stump-screen.md`; the three strongest independent ones are kept (no one sentence
rescues two of them: the first is the QA rule's arithmetic over objects, the second the pay rule's arithmetic over
annotators, the third the driver of video work).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| QA rejects an image when any one object is missed, and each correction re-checks every object before another full review, so rejections and review passes climb steeply with object count and small or occluded objects | 2026's rejection share by scene type carried to requests far denser than any 2026 project, one correction per rejection (N04, L36, L40) | QA review passes (missed and misplaced counts per review) against the object table (size and occlusion per object), and 2026's two crowded street projects as the dense tail | none | kept |
| Annotators are paid per object with a guaranteed hourly floor settled per worker-week, so on slow work the slower annotators are topped up and the top-up per image is a hinge over the spread of speeds | 2026's top-up share of piece pay carried to slower work, or the floor applied to the average annotator, who clears it (L40, N01) | payroll worker-week lines (paid hours, piece pay, top-up) against each annotator's passes in the task log | none | kept |
| Video is annotated by propagating boxes frame to frame, so frame time follows tracks entering and leaving, not objects on screen | frame time scaled by objects on screen at 2026's video rate, which fitted 2026's busy urban projects (L36, N05) | the 2026 video projects' object table (track ids per frame) against per-chunk times in the task log, with 2026's two calm parking-lot projects as the slice that separates the drivers | none | kept |
| The labelling tool stops its timer after 90 seconds without input, and annotators pause longer on crowded images, so tool time understates paid time most where images are dense | paid time per tool minute held at 2026's overall ratio | worker-day timesheet hours against the sum of tool time per worker-day | 1 (next to the closed card on values cut at a time limit) | dropped as a stump; kept as Layer 1 and a supporting step whose omission alone leaves the call standing |
| Each object takes longer when it overlaps others, and the crowded request overlaps far more | per-object time at 2026's average | object coordinates and per-object timestamps | 1 (the closed transport card: within-band rates carried to the target's mix), 2 (a pattern one group-by of one file shows, R14) | dropped |

## Tried and rejected

- 2026-11-13, at the draw: per-object time rising with overlap as a stump (dropped: it is the closed transport card's fix and a pattern one group-by shows); the tool's 90-second idle timer as a stump (dropped: next to the closed card on values cut at a time limit; kept as Layer 1 and a supporting step).
