"""submission.md: the four answer blocks, every figure emitted from figures.json."""
import core as C
import deliver
import docs
import pack

M = C.MEMBERS
F = pack.FILES


def lst(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def rng(b, nd=1):
    return "%.*f to %.*f" % (nd, b[0], nd, b[1])


def each(f, key, nd=2, boards=M):
    return ", ".join("%s %.*f" % (b, nd, key[b]) for b in boards)


def banded(vals, bands):
    return "; ".join("%s %.1f (%s)" % (b, vals[b], rng(bands[b])) for b in M)


def write(path, f):
    down = [b for b in M if f["side"][b] == "down"]
    up = [b for b in M if f["side"][b] == "up"]
    keep = [b for b in M if f["side"][b] == "as banked"]
    h = f["hurried"]["distance"]
    R, rf, nv = f["routes"], f["referee"], f["nearest_variant"]
    hd = [b for b in M if h[b] >= f["line"]]
    wb, csv = deliver.FILES["wb"], deliver.FILES["csv"]
    out = []
    w = out.append
    w("# task8 answer blocks\n")
    w("## Tags\n")
    w("**Domain:** Other, Education & Learning Sciences (psychometrics, test equating: six examining boards' "
      "centre-assessed marks linked to the marking standard of the board taking them over).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).\n")
    w("## Final Recommendation\n")
    w("**Convert %s banked marks down by %s marks, convert %s up by %s marks, and carry %s as banked (%s marks above "
      "Carrow's standard, inside the protocol's %.1f).** This rejects the boards' moderation records read as they stand, "
      "which leave Ardkeel as banked (%.1f marks) and convert %s down (%.1f to %.1f marks): a moderator's recorded "
      "difference is only part of the marking difference, a sample catches a centre in its highest-marking year, and "
      "each board moderates to its own standard, not Carrow's.\n" % (
          lst("%s's" % b for b in down), lst("%.1f" % f["converted"][b] for b in down),
          lst("%s's" % b for b in up), lst("%.1f" % f["converted"][b] for b in up), lst("%s's" % b for b in keep),
          lst("%.1f" % f["distance"][b] for b in keep), f["line"], h["Ardkeel"], lst(hd),
          min(h[b] for b in hd), max(h[b] for b in hd)))
    w("## Supplementary Questions\n")
    w("### %s\n" % wb)
    w("1. Each joining board's banked marks against Carrow's standard, the 2025 and 2026 series taken together, in marks "
      "(positive is above the standard; the range any sound set of estimating conventions gives is in brackets): %s." % (
          banded(f["distance"], f["distance_band"])))
    w("2. The same for each series. 2025: %s. 2026: %s." % (
        banded(f["by_series"]["2025"], f["by_series_band"]["2025"]), banded(f["by_series"]["2026"], f["by_series_band"]["2026"])))
    w("3. The joining boards as a whole stand %.1f marks above Carrow's standard (%s)." % (f["whole"], rng(f["whole_band"])))
    w("4. The workbook opens on the conversion: one row per joining board with its distance for the two series together "
      "and for each series, the protocol's outcome and the conversion, a row for the joining boards as a whole, and a "
      "column chart of the six distances against the %.1f-mark tolerance.\n" % f["line"])
    w("### %s\n" % csv)
    w("5. One row per centre of a joining board and series: the board, the national roll number, the series, the "
      "candidates with a banked mark, whether the centre was sampled in that series, and the centre's estimated distance "
      "from Carrow's standard in marks.\n")
    w("## Critical Components\n")
    w("1. Ardkeel's moderators record **%.1f per cent** of the difference a marker finds without the centre's marks "
      "(%s per cent), so a recorded sample difference is divided by the board's share before it is used." % (
          f["c1"], rng(f["c1_band"])))
    w("2. Fennor's centres mark **%.1f marks lower** in the year after a sample than in the sampled year (%s lower), so "
      "a centre not sampled in a banked series does not stand at its last sample." % (
          abs(f["c2"]), rng([abs(f["c2_band"][1]), abs(f["c2_band"][0])])))
    w("3. Gortavale's moderators mark to a standard **%.1f marks below** Carrow's (%s below), so its moderation "
      "measures its centres against another standard.\n" % (abs(f["c3"]), rng([abs(f["c3_band"][1]), abs(f["c3_band"][0])])))
    w("## Step-by-Step\n")
    rep = f["repeat_rows"]
    w("1. Brought the seven boards' files to one schema: series as a year, centres by national roll number "
      "(`%s`), one row per entry. That is %s mark sheet rows once the %d rows %s's system loaded twice are counted "
      "once; withdrawn and absent entries carry no mark (`%s`, 2.3); a reissued moderation record replaces the earlier "
      "one (`%s`, 4.5); Brannock's and Fennor's samples are unpacked from their delimited fields. Every sample's mean "
      "difference (centre's mark less moderator's, Code 4.1) reproduces its outcome, and an awarded mark is the "
      "centre's mark less the adjustment. On the samples of 2021 to 2026 the mean recorded differences are %s marks, "
      "and %d to %d per cent of sampled centres were adjusted." % (
          F["centres"], format(f["mark_rows_total"], ","), sum(rep.values()), lst(rep), docs.FILES["protocol"],
          docs.FILES["code"], each(f, f["recorded_mean"]), min(f["adjusted_pct"][b] for b in M),
          max(f["adjusted_pct"][b] for b in M)))
    w("2. The hurried reading stops at those records. The 2025 and 2026 samples as they stand, with adjustments netted, "
      "centres weighted by candidates and a centre not sampled in a series carried at its last sample, put the boards "
      "at %s marks, which leaves Ardkeel and converts the other five down. Three things about how a moderation record "
      "comes to hold what it holds overturn it (steps 3 to 5)." % each(f, h))
    w("3. What a sample difference measures. The sample record the moderator fills in lists the centre's marks (Code "
      "3.3, 3.4), while the standardisation scripts are the previous series' sampled portfolios marked by the whole "
      "team with no marks on them (Code 5.2, 5.3). Joined each script (the boards' standardisation scripts files) by "
      "its source series, centre and candidate to the same portfolio's row in the sample marks: %d scripts a board "
      "over the 2015 to 2026 meetings. The live recorded difference (centre less moderator) regressed on the "
      "difference found without the centre's marks (centre less the team's consensus before the meeting, the mean of "
      "the marks given on the script, a blank being a script that moderator did not reach) has a slope "
      "of %.1f per cent at Ardkeel (%s) and %s per cent at the others (one fit a board over all twelve meetings pooled, "
      "with a single intercept). Each recorded difference is divided by its "
      "board's share. Taking the recorded difference as the difference puts Ardkeel at %.2f marks and carries it as "
      "banked." % (f["trial_scripts"]["Ardkeel"], f["c1"], rng(f["c1_band"]),
                   ", ".join("%s %.1f" % (b, f["share_pct"][b]) for b in M if b != "Ardkeel"), R["S1"]["distance"]["Ardkeel"]))
    w("4. Where a centre stands between samples. The sample years rebuilt from the sample records give rotas of %s "
      "years (Carrow samples every year). From the mark sheets of the last nine series, the mean centre mark (the "
      "centre's own mark, before any adjustment, since a sample difference is measured on it) by years since the "
      "centre's last sample, each centre against itself and net of the board's year (a fit on the centre-series "
      "means with a centre effect and a series effect, each centre-series counted once), is lower after a sample: "
      "Fennor's centres by %.1f marks one year after (%s) and %.2f two years after; the first year after is %s marks "
      "lower at the others. A centre not sampled in a banked series is placed at its last sample over the share, plus "
      "the level for the years since. Carrying the last sample as it stands puts Fennor at %.2f marks and converts "
      "it." % (", ".join("%s %d" % (b, f["rota_years"][b]) for b in M), abs(f["c2"]),
               rng([abs(f["c2_band"][1]), abs(f["c2_band"][0])]), f["cycle_lower"]["Fennor"][1],
               ", ".join("%s %.2f" % (b, f["cycle_lower"][b][0]) for b in M if b != "Fennor"), R["S2"]["distance"]["Fennor"]))
    w("5. Whose standard. Each board's moderators apply their own principal's agreed marks (Code 5.4, 5.5) and no "
      "portfolio was marked by two boards. `%s` holds %d moderators appointed by two boards, in %d pairs of boards. For "
      "each such person and series, their marks less the team's consensus at each of their two boards' meetings, taken "
      "as a difference, give the gap between the two teams (%s person-series, 2020 to 2026); each board's consensus less "
      "its agreed marks (%s marks, the mean over its twelve meetings, 2015 to 2026) takes each side to its own "
      "standard; the ten links fitted together by least squares over the person-series, with Carrow at "
      "zero, put the boards' standards at %s marks against Carrow's (Gortavale's range %s). Taking each board's own "
      "principal as the standard puts the boards at %s marks and converts all six down." % (
          F["register"], f["two_board_people"], f["board_pairs"], format(f["link_people_years"], ","),
          each(f, f["agreed_gap"], 2, C.BOARDS), each(f, f["standard"]), rng(f["c3_band"]),
          each(f, R["S3"]["distance"])))
    w("6. Checked the route on a record it does not use. The regulator's 2023 review (`%s`, %s portfolios) marked "
      "every Dunmoyle centre at Carrow's standard. On the %d centres Dunmoyle did not sample in 2023 the review finds "
      "the centres' marks %.2f above Carrow's standard (centres weighted by their candidates, as throughout); steps 3 "
      "to 5 run for 2023 on the same centres give %.2f (%.2f away). The three shortcuts give %.2f, %.2f and %.2f, and "
      "the record with each board's own meeting severity (its consensus less its agreed marks) added gives %.2f." % (F["review"], format(f["review_portfolios"], ","), rf["unsampled_centres"], rf["review"], rf["golden"],
                       rf["off"], rf["rivals"]["S1 lost"]["value"], rf["rivals"]["S2 lost"]["value"],
                       rf["rivals"]["S3 lost"]["value"], rf["rivals"]["rigorous"]["value"]))
    w("7. Each centre's distance is its board's standard plus its level against that standard: for a centre sampled in "
      "the series, its recorded difference divided by the share, with the adjustment applied in that series then "
      "taken off (whole marks, as the mark sheet "
      "shows them); for the others, as in step 4 (`%s`, %s rows). Weighted by candidates with a banked mark (%s over the six boards), the boards stand %s marks "
      "above Carrow's standard for the two series together, and %.1f as a whole." % (
          csv, format(f["csv_rows"], ","), format(f["banked_total"], ","), each(f, f["distance"], 1), f["whole"]))
    w("8. Applied the protocol's 4.2: %s are %.1f marks or more above and convert down, %s is %.1f or more below and "
      "converts up, %s are inside. The nearest board to a tolerance is %s, %.2f marks from it." % (
          lst(down), f["line"], lst(up), f["line"], lst(keep), min(M, key=lambda b: f["margin"][b]), min(f["margin"].values())))
    w("9. Rebuilt the route in each of these ways (the share with or without an intercept, on the consensus or the agreed marks, as a "
      "ratio of means on the agreed marks, on the last six meetings, year by year; the levels on six, nine or twelve series, weighted or not, or "
      "from each centre's own change; one or two last samples; the links weighted, trimmed, at the median, on the 2023 "
      "to 2026 meetings, one link a board on its shortest path to Carrow, with or without a marker's own mark in the "
      "consensus; and every pair of these that changes two different choices): all "
      "give the same six outcomes, the nearest any of these rebuilds comes to a tolerance is %.2f marks (%s), and "
      "the stated ranges hold every one. Each fitted input moved by the furthest any rebuild moves it, alone and all three together, "
      "leaves the outcomes unchanged.\n" % (nv["distance"], nv["board"]))
    w("No other conversion survives the files. The moderation records as they stand pass every check they offer (each "
      "outcome reproduces from its sample, each joining board's team sits within a mark of its principal at the meeting, a centre's "
      "successive samples correlate at %.2f) and miss the one record that tests them: they put Dunmoyle's unsampled centres at "
      "%.2f marks in 2023 where the review found %.2f. Adding each board's own meeting severity to the record "
      "(%s marks) leaves Ardkeel and converts the other five, and is %.2f away from the review. Each single "
      "correction left out moves an outcome: without the share Ardkeel is carried, without the levels after a sample "
      "Fennor is converted, without the link all six convert down.\n" % (
          f["successive_samples"]["correlation"], rf["reflex"],
          rf["review"], each(f, R["rigorous"]["distance"]), rf["rivals"]["rigorous"]["off"]))
    pr, sm, ab, ca, rc = (f["rival_plain_ratio"], f["rival_share_by_moderator"], f["rival_awarded_base"],
                          f["rival_cycle_on_awarded"], f["rival_review_calibration"])
    nil = [b for b in M if sm["between"][b] == 0]
    some = [b for b in M if sm["between"][b] != 0]
    rs, bs = f["rival_recent_share"], f["beside"]
    w("Beside these, further rebuilds take the share from recent meetings alone or the levels from every series on file: "
      "the share fitted on the last five or the last four meetings (%.1f and %.1f per cent at Ardkeel) with every form of "
      "the links and of the levels in step 9 and with the levels on all fifteen series (a series before a centre's "
      "first filed sample placed by the board's rota); the share as a ratio of means on "
      "the agreed marks on the last six, five, four or three meetings (%.1f to %.1f per cent at Ardkeel); and the levels "
      "on all fifteen series (Fennor's centres %.2f marks lower in the year after a sample) alone and with each other "
      "choice of step 9. All give the same six outcomes, the nearest %.2f marks from a tolerance (%s), and the stated "
      "ranges are drawn to hold every one. On the last four meetings alone the boards stand at %s marks.\n" % (
          rs["five"]["share_pct"], rs["four"]["share_pct"], bs["ratio_share_pct"][0],
          bs["ratio_share_pct"][1], bs["fifteen_level"], bs["nearest"]["distance"], bs["nearest"]["board"],
          each(f, rs["four"]["distance"])))
    w("Five further readings were run. The share taken as a plain ratio of the mean live difference to the mean "
      "difference from the consensus as marked, with no use of the agreed marks, gives %s marks: the same outcomes, "
      "inside every stated range. The share fitted for each moderator reference with ten or more of the scripts (the "
      "same fit on their own scripts) and shrunk to the board's (the two weighted by the inverse of the fit's squared "
      "standard error and of the spread between moderators, that spread being the variance of the moderators' shares, "
      "taken over their number less one, less the mean of their squared standard errors, nil where that is negative; "
      "every other moderator at the board's share; a centre between samples at the share of its last sample's "
      "moderator) gives %s marks (the square root of the spread is nil at %s%s): the same outcomes, inside every range. With "
      "the awarded mark as the base throughout (a centre between samples placed at its last sample net of the "
      "adjustment applied then, plus a level fitted on the awarded marks) the boards stand at %s marks, again the same "
      "outcomes inside every range; adding awarded-mark levels to a last sample measured on the centre's own mark "
      "mixes the two bases, would convert Fennor (%.2f marks), and gives %.2f on the review's centres where the "
      "review found %.2f and the estimate gives %.2f. The review read as Dunmoyle's own answer gives %.2f marks for 2023 on every centre (the "
      "adjustments applied in 2023 netted), inside Dunmoyle's ranges, but "
      "it is one board in a series before the banked ones. The review used as a calibration set for the other boards "
      "(a share of %.1f per cent and a standard of %.2f marks read off Dunmoyle's centres sampled in 2023, carried to "
      "every board) files %s marks and wrong outcomes for %s: each board's own scripts and links give its own share "
      "(%.1f to %.1f per cent) and standard (%.2f to %.2f marks). Of the readings here that keep the outcomes, the "
      "nearest any board comes to a tolerance is %.2f marks (%s, on %s).\n" % (
          each(f, pr["distance"]), each(f, sm["distance"]), lst(nil),
          (", and " + lst("%.3f at %s" % (sm["between"][b], b) for b in some)) if some else "",
          each(f, ab["distance"]), ca["distance"]["Fennor"], ca["referee"], rf["review"], rf["golden"], rf["raw_all_centres"],
          rc["share_pct"], rc["standard"], each(f, rc["distance"]), lst(rc["boards_wrong"]),
          min(f["share_pct"][b] for b in M), max(f["share_pct"][b] for b in M),
          min(f["standard"][b] for b in M), max(f["standard"][b] for b in M),
          f["nearest_further"]["distance"], f["nearest_further"]["board"], f["nearest_further"]["reading"]))
    cs, nn = f["rival_consensus_standard"], f["rival_no_netting"]
    w("Two readings the filed text refuses would each move an outcome. A team's consensus taken as its board's standard "
      "in place of the principal's agreed marks puts Ardkeel at %.2f marks when only Carrow's standard is read that way "
      "(its team sits %.2f marks above its agreed marks) and at %.2f when every board's is, at the tolerance; the "
      "protocol's 3.1 and the Code's 5.4 make the principal's agreed marks the standard. The centre's own marks with no "
      "adjustment netted put the boards at %s marks, which would convert Fennor and carry Gortavale; the protocol's 2.1 "
      "makes the banked mark the mark awarded after moderation.\n" % (
          cs["carrow_only"]["Ardkeel"], cs["carrow_gap"], cs["every_board"]["Ardkeel"], each(f, nn["distance"])))
    om = f["rival_own_mark"]
    w("A third reading is refused by the files' own figures. The share fitted on the live moderator's own mark of the "
      "same script at the next meeting, in place of the team's consensus (%d to %d scripts a board; %s per cent), "
      "puts the boards at %s marks, would move %s, and gives %.2f on the review's centres, %.2f away against %.2f. One "
      "marker's mark is a noisy measure of the difference: on the same scripts the difference from the consensus "
      "regressed on the difference from that one mark has a slope of %.2f to %.2f, where a consensus is the mean of %d "
      "to %d marks. The shares divided by that slope (%s per cent) give %s marks, the outcomes of step 8, inside every "
      "stated range.\n" % (
          min(om["scripts"].values()), max(om["scripts"].values()), each(f, om["share_pct"], 1), each(f, om["distance"]),
          lst(om["boards_wrong"]), om["referee"], om["referee_off"], rf["off"], min(om["reliability"].values()),
          max(om["reliability"].values()), om["marks_a_script"][0], om["marks_a_script"][1],
          each(f, om["corrected_share_pct"], 1), each(f, om["corrected_distance"])))
    text = "\n".join(out)
    assert "—" not in text
    open(path, "w").write(text)
