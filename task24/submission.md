# task24 answer blocks

## Final Recommendation

Accept Shelfgrid Retail's shelf stills, Ardley Autonomy's highway video and Kestrin Warehousing's warehouse labels at the prices their clients offered (expected costs of delivery USD 4.24 an image, USD 0.0285 a frame and USD 0.31 an image, each under its offered price over 1.18), and decline Corvane Mobility's crowded street stills and Brindle Pallet Systems' pallet polygons unless their clients come up to at least USD 7.01 per image and USD 1.95 per image (expected costs USD 5.94 and USD 1.65); this rejects the costing that carries 2026's re-return share along the correction chain and prices video on the objects on screen, which accepts Corvane and declines the video.

## Supplementary Questions

1. The spreadsheet gives each request's expected cost of delivery per delivered image (per frame for the video request), to the cent per image and to a hundredth of a cent per frame, graded within plus or minus 3 per cent: Corvane USD 5.94 (80 per cent range 5.78 to 6.11); Shelfgrid USD 4.24 (80 per cent range 4.13 to 4.34); Ardley USD 0.0285 (80 per cent range 0.0275 to 0.0295); Brindle USD 1.65 (80 per cent range 1.61 to 1.69); Kestrin USD 0.31 (80 per cent range 0.30 to 0.32). The range is the expected cost's own uncertainty from the request's sample (its images resampled, the video's sequences resampled whole), graded loosely as a range that contains the expected cost and excludes each policy line.

2. Beside each cost it gives the drivers per delivered image (per frame for video): annotator paid minutes Corvane 54.4, Shelfgrid 38.8, Ardley 0.341, Brindle 22.0, Kestrin 2.4; QA reviews Corvane 2.86, Shelfgrid 2.29, Ardley 1.20, Brindle 1.08, Kestrin 1.07 (for the video, reviews per 25-frame task); floor top-up Corvane USD 0.763, Shelfgrid USD 0.390, Ardley USD 0.0005, Brindle USD 0.421, Kestrin USD 0.006. Minutes are graded within 5 per cent, reviews within 5 per cent, top-ups within 20 per cent or USD 0.005.

3. A sheet lists each 2026 project's actual cost per delivered unit (as payroll settled it, a week's pay and hours shared across projects by tool time, reviewers' pay by review time in each reviewer's local pay week) beside what the costing gives for that project's own images and annotators. It is graded on three projects that closed before the pull, within 5 per cent: P26-0446 (crowded street) actual USD 1.51, costing USD 1.48; P26-0441 (aerial) actual USD 1.57, costing USD 1.55; P26-0434 (parking-lot video) actual USD 0.0190 a frame, costing USD 0.0186. Across the 24 projects whose register end date falls by 18 October the costing is within 6 per cent on 23 and at most 6.9 per cent off; projects still running at the pull carry open correction chains (cost with no delivered image yet), so their actual runs high.

4. The April to October 2026 delivery cost as payroll settled it (pay weeks 6 April to 1 November 2026), to the dollar within 0.5 per cent: USD 192,217, made of piece pay USD 85,876, floor top-ups USD 7,052, QA reviewer pay USD 38,255 and overhead USD 61,034 (USD 1.55 on 28,252.4 annotator and 11,124.2 reviewer paid hours).

5. For each request to decline, the lowest price at which it could be accepted (1.18 times its expected cost), to the cent, within plus or minus 3 per cent: Corvane USD 7.01 per image; Brindle USD 1.95 per image.

6. The short note states the recommendation: accept Shelfgrid, Ardley and Kestrin; decline Corvane and Brindle.

## Critical Components

1. Each request's expected cost of delivery against its policy line (the offered price over 1.18): Corvane USD 5.94, over its line of USD 5.47; Shelfgrid USD 4.24, under its line of USD 4.62; Ardley USD 0.0285, under its line of USD 0.0331; Brindle USD 1.65, over its line of USD 1.51; Kestrin USD 0.31, under its line of USD 0.36.

2. QA reviews per delivered image on the crowded street and shelf requests: 2.86 and 2.29, because QA returns an image on any found issue and each correction re-checks every object, so a dense image's corrected version comes back far more often than 2026's typical one; carrying 2026's re-return share of corrected tasks (0.24) along the chain gives 2.23 and 2.10.

3. Annotator paid minutes per frame on the highway video: 0.341, because video work follows the tracks that start and end in each task, not the vehicles on screen; a rate on frames and objects on screen gives 0.608.

4. The costing checked on 2026's closed projects: on the parking-lot video P26-0434 it gives USD 0.0186 a frame against an actual USD 0.0190, where frame time on objects on screen gives USD 0.0416; on the crowded street P26-0446 it gives USD 1.48 against USD 1.51, where 2026's re-return share gives USD 1.41; within 6 per cent on 23 of 24 closed projects.

## Step-by-Step

1. Rebuild 2026 from the records: drop the task export's repeated rows and released tasks, read corrections by their parent pass, normalise the Iloilo QA desk's staff keys, take paid hours from the punch clock under the pay policy (one IN per five minutes, the supervisor's edit for a shift closed at midnight, lunch unpaid) and net the voided payroll re-run; the delivery cost closes at USD 192,217.

2. Fit per-object first-pass time by size and occlusion with each annotator's pace, correction time, review time, each annotator's tool share of paid time and the reviewers' paid time per review second (the careful pass gets these right).

3. QA: fit found-issue intensities per object type from 2026's reviews with each annotator's care, aggregate them over each sampled image (an image returns on any found issue), review each correction again at an intensity in proportion to the image's own (a correction re-checks every object) and run the chain to the fourth review: 2.86 reviews per image on the crowded street and 2.29 on the shelves. The hurried pass models the first-pass return on the object counts and carries 2026's re-return share of corrected tasks (0.24) along the chain, getting 2.23 and 2.10; a logistic of the re-return on the counts over-extrapolates to 3.45 and 2.86, and 2026's density bins land at 2.36 and 2.30.

4. The floor: for each annotator who would work a request (shares by contracted hours), set a week's piece pay at their pace against the centre's floor times their paid week, over their week-to-week variation, and average the top-ups: USD 0.421 an image on the pallet polygons and USD 0.763 on the crowded street; 2026's top-up share of piece pay (0.082) would miss the slow outlines.

5. Video: join the archive's tracks to each 25-frame task, regress task time on frames, objects on screen, tracks starting and tracks ending, and apply it to the sample's sequences: 0.341 paid minutes a frame. A rate on frames and objects on screen fits 2026's busy urban and plaza video and puts the highway at 0.608; the parking-lot project refutes it.

6. Cost each request (piece pay, top-ups, reviewers' paid time, USD 1.55 per paid hour) with its 80 per cent range, and check the costing on every 2026 project that closed before the pull (within 6 per cent on 23 of 24).

7. Hold each against its line: the crowded street and polygon requests cost more than their offered price over 1.18, the shelf, video and label requests less. Six defensible variants (care spread off, a lighter prior on care, no week-to-week variation, contracted rather than clocked weeks, video without track ends, reviewer time pooled) and every fitted input moved by its spread give the same set, while each hurried route gives a different wrong one, so no other conclusion survives.
