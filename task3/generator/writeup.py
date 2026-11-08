"""task3's submission.md, drafted from the figure set deliver.figures builds: every number is emitted, never typed.
The blocks run in the platform's order: Final Recommendation, Supplementary Questions, Critical Components,
Step-by-Step."""
import common as K
from deliver import comma, names


def write(R, F):
    cap = F["capacity"]
    top4 = [str(y) for y in F["top4"]]
    raw4 = [str(y) for y in F["raw_top4"]]
    L = ["## Tags", "",
         "**Domain:** Physical & Environmental Sciences, hydrology (flood frequency).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "",
         "## Final Recommendation", "",
         "**Build Alternative %s, the %s (capacity %s cfs): the design flow at Kinnard Road is about %s cfs once the "
         "record's storms are run through today's watershed.**" % (F["pick"], F["pick_barrels"], F["pick_capacity"],
                                                                   F["design_flow"]),
         "Not Alternative %s (%s cfs), which the gauge's %d annual peaks fitted as they stand would choose at %s cfs: "
         "they show no trend only because the paved watershed's faster floods and the lighter storms since 1990 "
         "cancel in them." % (F["raw_pick"], cap[F["raw_pick"]], F["n_years"], F["raw_q1"]),
         "", "## Supplementary Questions", "",
         "### %s" % K.DOCX_OUT, "",
         "1. States the design flow, about %s cfs (%s to %s cfs on every sound pairing of the storms with their "
         "floods), and recommends Alternative %s, %s, capacity %s cfs; Alternative A (%s cfs) would overtop and "
         "Alternative C (%s cfs) passes at greater cost." % (F["design_flow"], F["band_low"], F["band_high"],
                                                            F["pick"], F["pick_barrels"], F["pick_capacity"],
                                                            cap["A"], cap["C"]),
         "2. A chart of peak flow against return period: the frequency curve of the table the estimate rests on, the "
         "recorded peaks' curve beside it, both series' plotting positions, and the three capacities as lines.",
         "3. Names water year %d as the largest flood in the table the estimate rests on (%s cfs recorded, about %s "
         "cfs on today's watershed), not water year %d, the largest as recorded (%s cfs)." % (
             F["largest_year"], F["largest_recorded"], F["largest_today"], F["raw_largest_year"],
             F["recorded_largest"]),
         "4. The four largest in order: water years %s; as recorded the order would be %s." % (names(top4),
                                                                                              names(raw4)),
         "", "### %s" % K.CSV_OUT, "",
         "1. %d rows, one per water year %s; columns water_year, peak_date, recorded_peak_cfs and "
         "estimate_peak_cfs, the last the peak the estimate rests on: each "
         "recorded peak raised by the response's rise between that year's paved fraction and 2025's, to the "
         "nearest ten cfs; water year %d's row reads about %s cfs." % (F["n_years"], F["years"],
                                                                           F["largest_year"], F["largest_today"]),
         "", "## Critical Components", "",
         "1. The %d recorded annual peaks show no trend (Kendall's tau **%s**, p = **%s**) and fitted as they stand "
         "give **%s cfs**, under Alternative A's %s." % (F["n_years"], F["mk_tau"], F["mk_p"], F["raw_q1"], cap["A"]),
         "2. Paired with the rain gauge's storm totals, the same storm makes about **%s times** the peak on today's "
         "watershed that it made in 1960: the log peak rises **%s** per unit of paved fraction, which grew from **%s** "
         "to **%s per cent**." % (F["factor"], F["c"], F["imp_1956"], F["imp_2025"]),
         "3. On today's watershed the design flow is about **%s cfs** (**%s** to **%s** on every sound pairing), "
         "above Alternative A's **%s** and under Alternative %s's **%s**." % (F["design_flow"], F["band_low"],
                                                                            F["band_high"], cap["A"], F["pick"],
                                                                            F["pick_capacity"]),
         "4. Water year **%d** is the largest flood on today's watershed, not **%d**, the largest as recorded." % (
             F["largest_year"], F["raw_largest_year"]),
         "", "## Step-by-Step", "",
         "1. Read the Drainage Standard section 4: the design flow is the peak with a 1 per cent chance of being "
         "equalled or exceeded in any year of the crossing's first ten years of service (4.2), estimated from the "
         "gauge's record with the county's other records for the watershed (4.3); the least costly alternative whose "
         "capacity reaches it is recommended (4.5); capacities are in kinnard_road_culvert_alternatives.docx.",
         "2. Fitted the %d annual peaks in ollery_creek_annual_peak_flows.csv as they stand: Kendall's tau %s "
         "(p = %s), no trend, and the log-Pearson III 1 per cent flow %s cfs, which picks Alternative %s; the peaks "
         "since 1995 alone, the peaks regressed on the paved fraction or detrended in time all stay at or under %s "
         "cfs, the reasonable analysis that falls short." % (F["n_years"], F["mk_tau"], F["mk_p"], F["raw_q1"],
                                                           F["raw_pick"], F["rungs_high"]),
         "3. Rebuilt each year's paved fraction from tamsett_stormwater_impervious_parcels.xlsx (the Ollery basin's "
         "impervious area by the year it was built, a split parcel under both numbers counted once, over the "
         "basin's 11.5 square miles): %s per cent in 1956, %s in 2025." % (F["imp_1956"], F["imp_2025"]),
         "4. Paired the peaks in ollery_creek_peaks_above_base_1956-2025.csv (the 2009 and 2010 duplicate export "
         "counted once) with tamsett_rain_gauge_daily_1956-2025.csv's totals for the peak day and the two days before "
         "(the gauge in service, Monday accumulations spread): for the %d storms of an inch or more, the log peak "
         "rises %s per unit of paved fraction at a fixed storm, about %s times the 1960 peak for the same storm; the "
         "storms since 1990 also ran lighter, which is why the annual peaks hide it." % (F["n_pairs"], F["c"],
                                                                                        F["factor"]),
         "5. Put each annual peak on today's watershed by that rise and refitted log-Pearson III: the 1 per cent flow "
         "is about %s cfs, over Alternative A's %s and under Alternative %s's %s, so the county builds Alternative %s." % (
             F["design_flow"], cap["A"], F["pick"], F["pick_capacity"], F["pick"]),
         "6. Ranked the adjusted table: water year %d is the largest (%s cfs recorded, about %s cfs today), then %s; "
         "as recorded the order is %s." % (F["largest_year"], F["largest_recorded"], F["largest_today"],
                                          names(top4[1:]), names(raw4)),
         "",
         "No other conclusion survives. Every sound pairing of the storms with their floods (windows of two to four "
         "days, storms of half an inch to three inches, the annual peaks against their own storms, decade effects, "
         "log-Pearson III or the generalized extreme value) puts the design flow between %s and %s cfs, between "
         "Alternative A's and Alternative %s's capacities, and keeps water year %d first and the same four largest in "
         "the same order. Every route that fits the recorded peaks, however trimmed or detrended, stays at or under "
         "%s cfs, because the lighter storms of the last three decades hide the faster floods in the annual maxima; "
         "only setting each flood against its storm separates the two. Rebuilding only the storms since 1991 on "
         "today's watershed (%s cfs) would file Alternative A, but section 4.3 requires the full length of the "
         "gauge's record." % (F["band_low"], F["band_high"], F["pick"], F["largest_year"], F["rungs_high"],
                              F["recent_only"])]
    text = "\n".join(L) + "\n"
    F["sections"] = ["4.2", "4.3", "4.5", "4.6"]
    return text, F
