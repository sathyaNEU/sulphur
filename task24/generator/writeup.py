"""task24: submission.md, the four answer blocks, every figure read from figures.json's object."""

N = {"A": "Corvane Mobility's crowded street stills", "B": "Shelfgrid Retail's shelf stills",
     "C": "Ardley Autonomy's highway video", "D": "Brindle Pallet Systems' pallet polygons",
     "E": "Kestrin Warehousing's warehouse labels"}
SHORT = {"A": "Corvane", "B": "Shelfgrid", "C": "Ardley", "D": "Brindle", "E": "Kestrin"}
UNIT = {"A": "an image", "B": "an image", "C": "a frame", "D": "an image", "E": "an image"}


def m(x, k):
    return ("%.4f" % x) if k == "C" else ("%.2f" % x)


def listing(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def submission(G, F):
    req = "ABCDE"
    acc = F["call_accept"]
    dec = F["call_decline"]
    L = []
    L.append("# task24 answer blocks\n")
    L.append("## Final Recommendation\n")
    L.append("Accept %s at the prices their clients offered (expected costs of delivery %s, each under its offered price over "
             "1.18), and decline %s unless their clients come up to at least %s (expected costs %s); this rejects the costing "
             "that carries 2026's re-return share along the correction chain and prices video on the objects on screen, which "
             "accepts Corvane and declines the video.\n" % (
                 listing(N[k] for k in acc), listing("USD %s %s" % (m(F["R6_cost_%s" % k], k), UNIT[k]) for k in acc),
                 listing(N[k] for k in dec), listing("USD %s per image" % m(F["R7_lowest_price_%s" % k], k) for k in dec),
                 listing("USD %s" % m(F["R6_cost_%s" % k], k) for k in dec)))
    L.append("## Supplementary Questions\n")
    rows = "; ".join("%s USD %s (80 per cent range %s to %s)" % (SHORT[k], m(F["R6_cost_%s" % k], k),
                                                                 m(F["R6_range_%s" % k][0], k), m(F["R6_range_%s" % k][1], k))
                     for k in req)
    L.append("1. The spreadsheet gives each request's expected cost of delivery per delivered image (per frame for the video "
             "request), to the cent per image and to a hundredth of a cent per frame, graded within plus or minus 3 per cent: "
             "%s. The range is the expected cost's own uncertainty from the request's sample (its images resampled, the video's "
             "sequences resampled whole), graded loosely as a range that contains the expected cost and excludes each policy "
             "line.\n" % rows)
    L.append("2. Beside each cost it gives the drivers per delivered image (per frame for video): annotator paid minutes %s; QA "
             "reviews %s (for the video, reviews per 25-frame task); floor top-up %s. Minutes are graded within 5 per cent, "
             "reviews within 5 per cent, top-ups within 20 per cent or USD 0.005.\n" % (
                 ", ".join("%s %s" % (SHORT[k], ("%.3f" % F["R3_minutes_%s" % k]) if k == "C" else ("%.1f" % F["R3_minutes_%s" % k])) for k in req),
                 ", ".join("%s %.2f" % (SHORT[k], F["R2_reviews_%s" % k]) for k in req),
                 ", ".join("%s USD %s" % (SHORT[k], ("%.4f" % F["R4_topup_%s" % k]) if k == "C" else ("%.3f" % F["R4_topup_%s" % k])) for k in req)))
    L.append("3. A sheet lists each 2026 project's actual cost per delivered unit (as payroll settled it, a week's pay and hours "
             "shared across projects by tool time, reviewers' pay by review time in each reviewer's local pay week) beside what "
             "the costing gives for that project's own images and annotators. It is graded on three projects that closed before "
             "the pull, within 5 per cent: P26-0446 (crowded street) actual USD %.2f, costing USD %.2f; P26-0441 (aerial) actual "
             "USD %.2f, costing USD %.2f; P26-0434 (parking-lot video) actual USD %.4f a frame, costing USD %.4f. Across the %d "
             "projects whose register end date falls by 18 October the costing is within 6 per cent on %d and at most %.1f per "
             "cent off; projects still running at the pull carry open correction chains (cost with no delivered image yet), so "
             "their actual runs high.\n" % (
                 F["R5_actual_P26-0446"], F["R5_costing_P26-0446"], F["R5_actual_P26-0441"], F["R5_costing_P26-0441"],
                 F["R5_actual_P26-0434"], F["R5_costing_P26-0434"], F["R5_projects"], F["R5_within_6pct"], F["R5_max_gap_pct"]))
    L.append("4. The April to October 2026 delivery cost as payroll settled it (pay weeks 6 April to 1 November 2026), to the "
             "dollar within 0.5 per cent: USD %s, made of piece pay USD %s, floor top-ups USD %s, QA reviewer pay USD %s and "
             "overhead USD %s (USD 1.55 on %s annotator and %s reviewer paid hours).\n" % (
                 "{:,.0f}".format(F["R1_total"]), "{:,.0f}".format(F["R1_piece"]), "{:,.0f}".format(F["R1_topup"]),
                 "{:,.0f}".format(F["R1_reviewer"]), "{:,.0f}".format(F["R1_overhead"]), "{:,.1f}".format(F["R1_ann_hours"]),
                 "{:,.1f}".format(F["R1_rev_hours"])))
    L.append("5. For each request to decline, the lowest price at which it could be accepted (1.18 times its expected cost), "
             "to the cent, within plus or minus 3 per cent: %s.\n" % "; ".join(
                 "%s USD %s per image" % (SHORT[k], m(F["R7_lowest_price_%s" % k], k)) for k in dec))
    L.append("6. The short note states the recommendation: accept %s; decline %s.\n" % (
        listing(SHORT[k] for k in acc), listing(SHORT[k] for k in dec)))
    L.append("## Critical Components\n")
    L.append("1. Each request's expected cost of delivery against its policy line (the offered price over 1.18): %s.\n" % "; ".join(
        "%s USD %s, %s its line of USD %s" % (SHORT[k], m(F["R6_cost_%s" % k], k), "under" if k in acc else "over",
                                              m(F["line_%s" % k], k)) for k in req))
    L.append("2. QA reviews per delivered image on the crowded street and shelf requests: %.2f and %.2f, because QA returns an "
             "image on any found issue and each correction re-checks every object, so a dense image's corrected version comes "
             "back far more often than 2026's typical one; carrying 2026's re-return share of corrected tasks (%.2f) along the "
             "chain gives %.2f and %.2f.\n" % (F["R2_reviews_A"], F["R2_reviews_B"], F["rereturn_share_2026"],
                                                F["careful_reviews_A"], F["careful_reviews_B"]))
    L.append("3. Annotator paid minutes per frame on the highway video: %.3f, because video work follows the tracks that start "
             "and end in each task, not the vehicles on screen; a rate on frames and objects on screen gives %.3f.\n" % (
                 F["R3_minutes_C"], F["careful_minutes_C"]))
    L.append("4. The costing checked on 2026's closed projects: on the parking-lot video P26-0434 it gives USD %.4f a frame "
             "against an actual USD %.4f, where frame time on objects on screen gives USD %.4f; on the crowded street P26-0446 "
             "it gives USD %.2f against USD %.2f, where 2026's re-return share gives USD %.2f; within 6 per cent on %d of %d "
             "closed projects.\n" % (
                 F["R5_costing_P26-0434"], F["R5_actual_P26-0434"], F["R5_hurried_P26-0434"], F["R5_costing_P26-0446"],
                 F["R5_actual_P26-0446"], F["R5_hurried_P26-0446"], F["R5_within_6pct"], F["R5_projects"]))
    L.append("## Step-by-Step\n")
    steps = [
        "Rebuild 2026 from the records: drop the task export's repeated rows and released tasks, read corrections by their parent "
        "pass, normalise the Iloilo QA desk's staff keys, take paid hours from the punch clock under the pay policy (one IN per "
        "five minutes, the supervisor's edit for a shift closed at midnight, lunch unpaid) and net the voided payroll re-run; the "
        "delivery cost closes at USD %s." % "{:,.0f}".format(F["R1_total"]),
        "Fit per-object first-pass time by size and occlusion with each annotator's pace, correction time, review time, each "
        "annotator's tool share of paid time and the reviewers' paid time per review second (the careful pass gets these right).",
        "QA: fit found-issue intensities per object type from 2026's reviews with each annotator's care, aggregate them over each "
        "sampled image (an image returns on any found issue), review each correction again at an intensity in proportion to the "
        "image's own (a correction re-checks every object) and run the chain to the fourth review: %.2f reviews per image on the "
        "crowded street and %.2f on the shelves. The hurried pass models the first-pass return on the object counts and carries "
        "2026's re-return share of corrected tasks (%.2f) along the chain, getting %.2f and %.2f; a logistic of the re-return on "
        "the counts over-extrapolates to %.2f and %.2f, and 2026's density bins land at %.2f and %.2f." % (
            F["R2_reviews_A"], F["R2_reviews_B"], F["rereturn_share_2026"], F["careful_reviews_A"], F["careful_reviews_B"],
            F["alt_logit_reviews_A"], F["alt_logit_reviews_B"], F["alt_binned_reviews_A"], F["alt_binned_reviews_B"]),
        "The floor: for each annotator who would work a request (shares by contracted hours), set a week's piece pay at their pace "
        "against the centre's floor times their paid week, over their week-to-week variation, and average the top-ups: USD %.3f "
        "an image on the pallet polygons and USD %.3f on the crowded street; 2026's top-up share of piece pay (%.3f) would miss "
        "the slow outlines." % (F["R4_topup_D"], F["R4_topup_A"], F["topup_share_2026"]),
        "Video: join the archive's tracks to each 25-frame task, regress task time on frames, objects on screen, tracks starting "
        "and tracks ending, and apply it to the sample's sequences: %.3f paid minutes a frame. A rate on frames and objects on "
        "screen fits 2026's busy urban and plaza video and puts the highway at %.3f; the parking-lot project refutes it." % (
            F["R3_minutes_C"], F["careful_minutes_C"]),
        "Cost each request (piece pay, top-ups, reviewers' paid time, USD 1.55 per paid hour) with its 80 per cent range, and check "
        "the costing on every 2026 project that closed before the pull (within 6 per cent on %d of %d)." % (
            F["R5_within_6pct"], F["R5_projects"]),
        "Hold each against its line: the crowded street and polygon requests cost more than their offered price over 1.18, the "
        "shelf, video and label requests less. Six defensible variants (care spread off, a lighter prior on care, no week-to-week "
        "variation, contracted rather than clocked weeks, video without track ends, reviewer time pooled) and every fitted input "
        "moved by its spread give the same set, while each hurried route gives a different wrong one, so no other conclusion "
        "survives."]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s\n" % (i, s))
    return "\n".join(L)
