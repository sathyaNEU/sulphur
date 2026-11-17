"""submission.md: the tags and the four answer blocks, every figure from figures.json."""
import deliver
import docs
import pack

F = dict(pack.FILES)
F.update(docs.FILES)
WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _rng(xs, nd=2):
    xs = list(xs)
    return "%.*f to %.*f" % (nd, min(xs), nd, max(xs))


def _b(band, nd):
    return "%.*f to %.*f" % (nd, band[0], nd, band[1])


def write(path, f):
    names = deliver.order(f)
    by, st, so, R, n = f["by_class"], f["stations"], f["sources"], f["routes"], f["counts"]
    reg, ref, acc = f["regulation"], f["referee"], f["account_residual"]
    t = reg["times_a_season"]
    lo, hi = reg["lines"]
    refl = R["S1+S2+S3"]
    down = [s for s in sorted(names, key=lambda s: -f["storms"][s]) if refl[s]["class"] != f["classes"][s]]
    L = ["# task3 answer blocks", "", "## Tags", "",
         "**Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (extreme-value and "
         "environmental-hazard analysis: how often a short-duration rain depth is exceeded at ungauged source areas).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "", "## Final Recommendation", ""]
    L.append(
        "**Class 3 (automatic barrier) at %s, class 2 (seasonal patrol with hand gates) at %s and class 1 (signs) at %s for "
        "the 2027 to 2031 program**: the triggering storms a season to expect are %s, against the regulation's lines of "
        "%.1f and %.1f. This rejects the classing with barriers only at %s (%s), which the tip records give when each station "
        "is scaled by the one factor that closes its storage gauge account, carried to its source areas by the ratio of "
        "their yearly rainfall and read as rain on hail days: the buckets lose more the harder it rains, a source area's "
        "cloudbursts stand to its station's by a factor the yearly rainfall does not carry, and on hail days the tips "
        "come after the storm has gone." % (
            _list(by["3"]), _list(by["2"]), _list(by["1"]),
            _list("%s %.2f" % (s, f["storms"][s]) for s in sorted(names, key=lambda s: -f["storms"][s])), hi, lo,
            _list(s for s in names if refl[s]["class"] == 3),
            _list("%s %.2f" % (s, refl[s]["storms"]) for s in down)))
    L += ["", "## Supplementary Questions", "", "### %s" % deliver.FILES["wb"], ""]
    L.append("1. The first sheet states the classing: one row per crossing with its class, the triggering storms a season "
             "to expect and the 60-minute rain depth its source area reaches %s times a season, with a chart of the seven "
             "counts against the %.1f and %.1f lines." % (WORD[t], lo, hi))
    L += ["", "### %s" % deliver.FILES["csv"], ""]
    L.append("2. Seven rows, one per crossing: the class, the triggering storms a season to expect and the 60-minute rain "
             "depth, in mm, that the source area reaches %s times a season. Each figure's band is in brackets." % WORD[t])
    for i, s in enumerate(names):
        L.append("%d. %s (%s): class %d; %.2f triggering storms a season (%s); %.1f mm (%s)." % (
            3 + i, s, f["crossing_id"][s], f["classes"][s], f["storms"][s], _b(f["storms_band"][s], 2), f["depth"][s],
            _b(f["depth_band"][s], 1)))
    L += ["", "## Critical Components", ""]
    L.append("1. At a true %d mm an hour the Valfosca tipping bucket fails to record **%.1f per cent** of the rain (band %s)."
             % (f["stated"]["rate_mm_h"], f["under_read_valfosca_pct"], _b(f["under_read_valfosca_band"], 1)))
    L.append("2. The Rio Marden source area's 60-minute burst depths are **%.2f** times those at its governing station, "
             "Pradalt (band %s)." % (f["burst_factor_marden"], _b(f["burst_factor_marden_band"], 2)))
    L.append("3. Over Costarossa's hail and graupel storms of the %d warm seasons, the largest 60-minute depths read from "
             "the tips fall **%.1f per cent** short, sum against sum and with the loss put back on both sides, of those "
             "with each storm's water placed where the detector saw it fall (band %s)." % (n["seasons"], f["hail_gap_costarossa_pct"], _b(f["hail_gap_costarossa_band"], 1)))
    L += ["", "## Step-by-Step", ""]
    vfo, csr = st["Valfosca"], st["Costarossa"]
    sm = acc["small_bucket"]
    rt = acc["ratio"]
    kb = {d["bucket_mm"]: d["loss_h_per_mm"] for d in st.values()}
    mar, sas = so["Rio Marden"], so["Rio Sass"]
    riv, oth = ref["rivals"], ref["others"]
    mp, rdr = f["mapped_route"], f["radar_route"]
    away = [d["pct"] for k, d in mp["station"].items() if k != "Rio Scuro"]
    away1 = [d["pct"] for k, d in rdr["station"].items() if k != "Rio Scuro"]
    win = f["window"]
    hv = {how: [max(so[s]["halves"][how][i] for s in names) for i in (0, 1)] for how in ("qq", "pairs")}
    p = f["perturbations"]
    vr = f["variant_range"]
    steps = [
        "Read the six tip logs (`%s` and the others, %s rows; the loggers keep UTC+1 all year per `%s`, the visit book is in "
        "local civil time, the radar and the weighing gauges in UTC): rows a logger sent twice counted once (%s rows) and "
        "the tips in the hour after a visit with a tip test entered in `%s` left out (%s tips). Cut at six hours without "
        "rain (regulation 2.2, `%s`), the record holds %s storms a station; no dry gap in it lies between three and "
        "eight hours." % (
            F["tips"] % "VFO", format(n["tip_rows"], ","), F["stations"], format(sum(d["resent"] for d in st.values()), ","),
            F["visits"], format(sum(d["tests"] for d in st.values()), ","), F["regulation"],
            "%s to %s" % (format(min(d["storms"] for d in st.values()), ","), format(max(d["storms"] for d in st.values()), ","))),
        "Set each station's tips against its storage gauge between an emptying and the next read in `%s` (%d visit "
        "intervals): the storage gauge holds %s times the tipped water by station (Valfosca %.3f)." % (
            F["visits"], n["intervals"], _rng((d["account_factor"] for d in st.values()), 3), vfo["account_factor"]),
        "That one factor closes each station's total and leaves its intervals open by %s mm (rms), and what is left over "
        "runs with how hard the interval's rain fell (correlation %s with the sum, over the interval's minutes, of the "
        "tipped depth times its rate). Fitted the loss as time lost at each tip, one value a bucket model, by least "
        "squares on the intervals of the model's stations through the same account, on the minute-by-minute rates of "
        "the tips (a tip's stamp read as the end of its second; a tip's water laid evenly from the stamp of the tip "
        "before in the same storm to its own, a storm's first tip in its own second; minutes on the loggers' clock): a "
        "recorded rate r stands for r / (1 - k r), k %.6f hours per mm on the %.1f mm buckets and %.6f on "
        "the %.1f mm buckets, and the intervals close to %s mm. At a true %d mm an hour Valfosca's bucket fails to record "
        "%.1f per cent. The hurried route scales every minute by the one factor (%.2f per cent at any rate) and puts Rio "
        "Gelt at %.2f storms a season, class %d. Other ways of the loss were refitted through the same account and "
        "scored on the %s mm buckets, where the fitted reading leaves %.2f mm: read tip by tip or on totals of two, "
        "three or five minutes it leaves %.2f to %.2f mm and is among the rebuilds of step 8; written first-order in "
        "the rate on the same readings it leaves %.2f to %.2f mm (%.2f to %.2f times the tipping-time form's on the "
        "same reading), which does not rule it out, so the bands hold it; as a power law of the recorded rate (a scale "
        "and an exponent) on the same readings it leaves %.2f to %.2f mm, and the tipping-time form on 10- or 15-minute "
        "totals %.2f to %.2f mm with the loss free up to %s hours per mm (a tighter limit leaves more), so neither is "
        "used: every way used or held in the bands leaves %.2f mm or less and every way refused %.2f mm or more. Every "
        "one of these files the same seven classes." % (
            _rng(d["resid_factor"] for d in st.values()), _rng(d["resid_r"] for d in st.values()),
            kb[0.1], 0.1, kb[0.2], 0.2, _rng(d["resid_rate"] for d in st.values()), f["stated"]["rate_mm_h"],
            f["under_read_valfosca_pct"], vfo["one_factor_pct"], R["S1"]["Rio Gelt"]["storms"], R["S1"]["Rio Gelt"]["class"], sm,
            acc["golden"][sm], acc["kept"][sm][0], acc["kept"][sm][1],
            acc["refused"]["first-order form"][sm][0], acc["refused"]["first-order form"][sm][1],
            rt["first-order form"][0], rt["first-order form"][1],
            acc["refused"]["power law"][sm][0], acc["refused"]["power law"][sm][1],
            min(acc["refused"]["10-minute totals"][sm][0], acc["refused"]["15-minute totals"][sm][0]),
            max(acc["refused"]["10-minute totals"][sm][1], acc["refused"]["15-minute totals"][sm][1]),
            ("%.4f" % acc["k_limit"]), acc["held_max"], acc["refused_min"]),
        "Marked the storms with a hail or graupel code in any ten-minute block of `%s` (codes in `%s`): %d to %d a station "
        "in the warm seasons, %d at Costarossa. On a station's hail storms, in season or out, %.1f to %.1f per cent of "
        "the tipped water (spread and loss put back as in step 3; a minute's water counted in the ten-minute block "
        "that holds its first second, and water tipped before the storm's first block with that block) lies in "
        "blocks for which the detector holds no row, against %.2f to %.2f per cent on rain storms. Kept each such storm's "
        "tipped water, loss put back, and placed it on the blocks in which the detector saw precipitation, in proportion "
        "to its intensity, so that a hail storm's largest 60-minute depth is the largest total of six consecutive "
        "ten-minute blocks; read from the tips, those storms' largest 60-minute depths fall %.1f per cent short at "
        "Costarossa. The hurried route reads the tips as rain where they stand and puts Rio Bianc at %.2f, class %d. "
        "Four other placings were set against the Rio Scuro weighing gauges of step 7, which saw %d storms reach their "
        "depths where this placing counts %d: the detector's own amounts, scaled by the station's tipped water over "
        "the detector's on its rain storms, count %d (on rain storms they scatter about the tips by %.2f on logs); "
        "every drop laid on the hail-coded blocks alone, by their intensity, %d; the water left as tipped in the "
        "blocks the detector saw wet and only the rest moved, onto the hail-coded blocks by their intensity, %d; and "
        "the water shared equally among the wet blocks %d, which would put Rio Bianc at %.2f. None is used; the "
        "hail-coded blocks alone file the same seven classes and the bands hold them." % (
            F["pw"], F["wx"], min(d["hail_storms"] for d in st.values()), max(d["hail_storms"] for d in st.values()),
            csr["hail_storms"], min(d["late_hail_pct"] for d in st.values()), max(d["late_hail_pct"] for d in st.values()),
            min(d["late_rain_pct"] for d in st.values()), max(d["late_rain_pct"] for d in st.values()),
            f["hail_gap_costarossa_pct"], R["S3"]["Rio Bianc"]["storms"], R["S3"]["Rio Bianc"]["class"],
            ref["seen"]["storms"], ref["golden"]["storms"], oth["the detector's own amounts on hail storms"]["storms"],
            max(d["optical_log_sd"] for d in st.values()), oth["hail water laid on the hail-coded blocks alone"]["storms"],
            oth["hail water moved only from the dry intervals"]["storms"], oth["hail water spread evenly"]["storms"],
            f["crude"]["hail even"]["storms"]["Rio Bianc"]),
        "For each source area in `%s`, took the cells of `%s` (pixels through `%s`, which also carries the identifiers used "
        "to 2018) with 1 mm or more in both the source area's pixel and its governing station's pixel, %d to %d cells a "
        "crossing, and the mean ratio of the two on logs: %.2f at Rio Marden against Pradalt, where the yearly rainfall of "
        "`%s` gives %.2f, and %.2f at Rio Sass, where it gives %.2f. The hurried route carries each station uphill by the "
        "yearly rainfall's ratio and puts Rio Marden at %.2f, class %d, and Rio Sass at %.2f, class %d. The radar's own "
        "depths are not counted against the triggering depths: a pixel is a square kilometre and the triggering depth is a "
        "point depth. Adjusted to the stations by one factor (the stations' depths after their storage gauge factor, "
        "summed, over the radar's on the stations' pixels in the same cells) and counted at the source pixels over the "
        "radar's %d seasons they leave %s barriers; matched rank for rank, largest first, with what the four Rio Scuro "
        "weighing gauges recorded (the cells' depths on the gauges' pixels against the gauges' depths, both pooled, read "
        "linearly between ranks) and counted the same way they leave %s (Rio Gelt %.2f, Rio Marden %.2f, Rio Bianc %.2f "
        "storms a season). Both adjustments meet the Rio Scuro gauges of step 7 (%d and %d storms against the %d "
        "seen), so the gauges do not rule on them; the stations' own pixels do. Set on each station's own pixel, the "
        "gauge-matched depths file %d storms of %d mm at Rio Scuro where the station's own depths (steps 3 and 4) hold "
        "%d in the same cells, and %d to %d per cent of the station's storms at the other five; the one-factor depths "
        "file %d per cent at Rio Scuro and %d to %d per cent at the other five; and the radar's scatter "
        "about the station's depth, on cells of 3 mm or more at the station, runs from %.2f on logs at %s to %.2f at "
        "Rio Scuro. The two pixels' depths matched rank for rank without pairing the storms are not used either (each "
        "station storm's depth times the ratio of the source pixel's depth to the station pixel's at the storm's own "
        "rank position among the station's storms, mid-rank over their number, each pixel's cells sorted on their own "
        "and read linearly at that position): made on the cells of the odd years alone and of the even years alone, "
        "that carry's two versions differ by up to %.1f mm in a crossing's depth reached %s times a season and by up "
        "to %.2f in its storms a season, the paired mean's by up to %.1f mm and %.2f." % (
            F["crossings"], F["radar"], F["pixels"], min(so[s]["pairs"] for s in names), max(so[s]["pairs"] for s in names),
            mar["burst_factor"], F["normal"], mar["normal_ratio"], sas["burst_factor"], sas["normal_ratio"],
            R["S2"]["Rio Marden"]["storms"], R["S2"]["Rio Marden"]["class"], R["S2"]["Rio Sass"]["storms"],
            R["S2"]["Rio Sass"]["class"], n["radar_years"][1] - n["radar_years"][0] + 1,
            WORD[int(f["route_class_counts"]["radar"]["3"])], WORD[int(f["route_class_counts"]["mapped"]["3"])], mp["storms"]["Rio Gelt"], mp["storms"]["Rio Marden"],
            mp["storms"]["Rio Bianc"], oth["the radar product"]["storms"], oth["the radar mapped on these same gauges"]["storms"],
            ref["seen"]["storms"], mp["station"]["Rio Scuro"]["route"], mp["at_mm"], mp["station"]["Rio Scuro"]["station"],
            min(away), max(away), rdr["station"]["Rio Scuro"]["pct"], min(away1), max(away1),
            min(d["scatter"] for d in mp["station"].values()),
            min(mp["station"], key=lambda k: mp["station"][k]["scatter"]), mp["station"]["Rio Scuro"]["scatter"],
            hv["qq"][1], WORD[t], hv["qq"][0], hv["pairs"][1], hv["pairs"][0]),
        "Took each storm's largest depth over 60 consecutive minutes at the governing station (regulation 2.3: 60 "
        "consecutive minutes of the logger's clock, and on a hail storm the six consecutive blocks of step 4), times the "
        "source area's burst factor, and counted the storms of 1 May to 31 October, %d to %d, that reach the register's "
        "triggering depth: %s storms, which over %d warm seasons (regulation 3.1) are the storms a season of the "
        "Supplementary Questions. The depth reached %s times a season (regulation 3.2) is the %dth largest of those "
        "%d seasons. With a tip's stamp read as the start of its second, or the 60 minutes slid by the second, a count "
        "moves by %s at up to %s crossings and a depth by up to %.2f mm; no class moves and the bands hold both." % (
            n["first_year"], n["last_year"],
            _list("%s %d" % (s, f["storm_count"][s]) for s in sorted(names, key=lambda s: -f["storm_count"][s])),
            n["seasons"], WORD[t], n["even_rank"], n["seasons"],
            "one storm" if win["storms_moved"] == 1 else "up to %s storms" % WORD[win["storms_moved"]],
            WORD[win["crossings_moved"]], win["depth_moved_mm"]),
        "Checked the whole route where the answer is on file: `%s` holds weighing gauges at %s source areas above the Rio "
        "Scuro station for %d seasons, with their own triggering depths in `%s`. The gauges saw %d storms reach those "
        "depths; the depth a gauge reaches %s times a season (its %dth largest storm of the %d seasons) averages %.2f mm "
        "over the four gauges, and the mean of a gauge's %d largest storms averages %.2f mm. The route gives %d, %.2f "
        "and %.2f. With one factor for the bucket it gives %d storms, with the yearly rainfall's ratio %d and with "
        "hail days read as rain %d." % (
            F["rs_events"], WORD[ref["gauges"]], ref["seasons"], F["rs_gauges"], ref["seen"]["storms"],
            WORD[t], ref["rank"], ref["seasons"], ref["seen"]["depth"], ref["rank"], ref["seen"]["top"],
            ref["golden"]["storms"], ref["golden"]["depth"], ref["golden"]["top"],
            riv["bucket put back by one factor"]["storms"], riv["source scaled by the rainfall normal"]["storms"],
            riv["tips taken as rain on hail days"]["storms"]),
        "Classed each crossing on regulation 4.1: %s at %.1f or more, %s between %.1f and %.1f, %s under %.1f. Rebuilt the "
        "route %s ways (the rate read tip by tip and on totals of one, two, three and five minutes; a tip's water in its "
        "own minute; the loss with a fixed factor beside it; one loss a station; the burst factor as a median, a ratio of "
        "sums, a mean trimmed by a tenth at each end, on cells of 3 mm or more at the station's pixel or at both, on the "
        "upper quarter of the pairs by their joint size, and each storm carried by its own pixel pair; the hail storms' "
        "water placed by the detector's intensity with the hail-coded blocks weighted by the one factor that closes "
        "those storms' tipped totals, or left as tipped before the first hail-coded block and placed by the detector's "
        "intensity from it on, or those storms' depths as tipped raised by one multiplier, the Rio Scuro gauges over "
        "the station on hail storms against the same on rain storms): "
        "every one files the same seven classes (%s), and the nearest any crossing comes to a line is %.2f storms a "
        "season. Each band covers these rebuilds and the ways steps 3 and 4 hold, crossed with them and with each "
        "other, with room above the highest for one more storm or a tenth of a millimetre. With the fitted loss, the burst factors' distance from one or the hail storms' correction moved by %d per "
        "cent either way, the classes stay." % (
            _list(by["3"]), hi, _list(by["2"]), lo, hi, _list(by["1"]), lo, format(f["variants"], ","),
            "; ".join("%s %.2f to %.2f" % (s, vr[s][0], vr[s][1]) for s in names), f["nearest_variant"]["distance"],
            f["stated"]["moved_pct"]),
    ]
    for i, s in enumerate(steps):
        L.append("%d. %s" % (1 + i, s))
    L += ["",
          "No other classing survives the files. One factor a station closes the storage gauge totals and so passes its own "
          "check, yet it leaves the intervals with hard rain short in the same account and undercounts the Rio Scuro "
          "gauges' storms (%d against %d). The yearly rainfall's ratio is a filed, mapped quantity, and the radar's cells "
          "show the bursts do not follow it (Rio Marden %.2f against %.2f; at Rio Scuro it would count %d storms where the "
          "gauges saw %d). Reading hail days as rain keeps every storm's total and loses its timing, which the detector "
          "holds and the weighing gauges confirm (%d against %d). The tips as logged fall short of the gauges as well "
          "(%d). The radar's depths cannot stand in for the stations': matched to the Rio Scuro gauges they file %d to "
          "%d per cent of the stations' own storms of %d mm on the other five stations' pixels, and the radar holds %d "
          "of the %d seasons regulation 3.1 counts. All three shortcuts together leave %s barriers where the estimate "
          "files %s." % (
              riv["bucket put back by one factor"]["storms"], ref["seen"]["storms"], mar["burst_factor"], mar["normal_ratio"],
              riv["source scaled by the rainfall normal"]["storms"], ref["seen"]["storms"],
              riv["tips taken as rain on hail days"]["storms"], ref["seen"]["storms"],
              riv["the gauge read raw"]["storms"], min(away), max(away), mp["at_mm"],
              n["radar_years"][1] - n["radar_years"][0] + 1, n["seasons"], WORD[int(f["route_class_counts"]["S1+S2+S3"]["3"])],
              WORD[int(f["route_class_counts"]["golden"]["3"])]), ""]
    open(path, "w").write("\n".join(L))
