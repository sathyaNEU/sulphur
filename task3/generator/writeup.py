"""task3: submission.md, the four answer blocks, every figure from figures.json."""


def fmt(v):
    return "{:,}".format(int(v))


def text(F):
    sp = {int(k): v for k, v in F["spans"].items()}
    V = F["variants"]
    call = F["call_span_ft"]
    D = F["default"]
    top = F["top2"]
    lines = []
    a = lines.append
    a("# task3 submission: Durrow Creek bridge span")
    a("")
    a("## Tags")
    a("")
    a("**Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (extreme-value and "
      "environmental-hazard return-period analysis: flood frequency at an ungauged site).")
    a("**Analytical objective:** Forecasting & Predictive Modeling.")
    a("")
    a("## Final Recommendation")
    a("")
    a("**Build the %d ft span.** Durrow Creek's 1 per cent annual exceedance flood at Ransom Bar Road is about **%s cfs** "
      "once the Coyner River's record is carried to the creek flood by flood, at the rain each storm put on each basin "
      "below its snow line, which is above the 140 ft span's rated %s cfs and inside the %d ft span's %s cfs; this rejects "
      "the 140 ft span that the drainage-area transfer of the river's curve (about %s cfs) would choose, because the "
      "river's floods drained rain over only about half of its high basin while the foothill creek drains whole, and the "
      "240 ft span that a snow line placed with the standard atmosphere's %.1f degrees C per kilometre (about %s cfs) "
      "would choose." % (call, fmt(F["q01_5000"]), fmt(sp[140]), call, fmt(sp[call]), fmt(F["drainage_area"]),
                         F["constants"]["textbook_lapse"], fmt(V["lapse_6.5"]["q01_5000"])))
    a("")
    a("## Supplementary Questions")
    a("")
    a("### durrow_creek_bridge_hydrology_report.pdf")
    a("")
    a("1. The report recommends the %d ft span: its rated flow (%s cfs) carries the creek's 1 per cent flood and the "
      "140 ft span's (%s cfs) does not; it gives the basin (%.1f square miles), the record carried (the Coyner River near "
      "Tessel, USGS 12183450), how each flood was carried, the flows as a table with a chart of the creek's frequency curve "
      "against the three spans' rated flows, the span table and the creek's largest floods." % (
          call, fmt(sp[call]), fmt(sp[140]), F["area_c"]))
    a("2. The creek's 50 per cent annual exceedance flow: %s cfs." % fmt(F["q50_5000"]))
    a("3. The creek's 1 per cent annual exceedance flow: %s cfs." % fmt(F["q01_5000"]))
    for i, s_ in enumerate(sorted(sp), start=4):
        a("%d. The %d ft span (rated %s cfs): its rated flow would be exceeded %s." % (i, s_, fmt(sp[s_]), F["bands"][str(s_)]))
    a("7. The creek's two largest floods since 1951 came in water years %d and %d." % tuple(top))
    a("")
    a("### durrow_creek_estimated_annual_peaks.csv")
    a("")
    a("8. Seventy-five rows, one per water year from %d to %d in order, columns water_year, estimated_peak_flow_cfs "
      "(to the nearest 100 cfs), qualifier, coyner_river_peak_date and coyner_river_peak_cfs (the date and peak of the "
      "Coyner River flood carried); water year %s holds no flood fed by rain and is given as less than the low-flood "
      "threshold (qualifier \"<\"); the two largest values are water years %d and %d, the same floods the report "
      "names." % (F["constants"]["first_wy"], F["constants"]["last_wy"],
                  " and ".join(str(y) for y in F["missing_years"]), top[0], top[1]))
    a("")
    a("## Critical Components")
    a("")
    a("1. Durrow Creek's 1 per cent flood is about **%s cfs**, against rated flows of **%s**, **%s** and **%s cfs** for "
      "the 140, 185 and 240 ft spans, so the %d ft span is the shortest that carries it." % (
          fmt(F["q01_5000"]), fmt(sp[140]), fmt(sp[185]), fmt(sp[240]), call))
    a("2. In the Coyner River's floods only about **half** of its basin drained rain (a median **%d per cent**; the rest "
      "lay above the storm's snow line) against **all** of Durrow Creek's, so the creek's 1 per cent flood is about a "
      "third larger than the river's own **%s cfs**, not the same size." % (F["share_river_median_pct"], fmt(F["river_1pct"])))
    a("3. Each flood's snow line comes from the airport's hourly temperature while its rain fell, with the storm lapse "
      "rate the station pair shows on storm days (about **%.1f degrees C per kilometre**, well below the standard "
      "atmosphere's %.1f) and the SNOTEL pillows' rain-snow temperature (about **%.1f degrees C**)." % (
          F["lapse_1"], F["constants"]["textbook_lapse"], F["t50_1"]))
    a("4. The creek's two largest floods since 1951 came in water years **%d** and **%d**, not in the Coyner River's "
      "record years (%d and %d)." % (top[0], top[1], F["river_top2"][0], F["river_top2"][1]))
    a("")
    a("## Step-by-Step")
    a("")
    a("1. Fitted Bulletin 17C to the Coyner River's %d annual peaks in usgs_12183450_coyner_r_annual_peaks.txt (expected "
      "moments, station skew weighted with the regional skew of %.2f in wsdot_region3_flood_frequency_excerpt.pdf): the "
      "river's 1 per cent flood is %s cfs." % (F["river_par"]["n"], F["regional_skew"], fmt(F["river_1pct"])))
    a("2. The reasonable but insufficient route: carried that curve to the creek by drainage area "
      "(region3_basin_characteristics.xlsx, %.1f against %.1f square miles) and got about %s cfs, the 140 ft span, with "
      "the river's record years as the creek's largest floods; the same transfer reproduces the region's other gauged "
      "basins because all of them are high basins like the river's." % (F["area_c"], F["area_r"], fmt(F["drainage_area"])))
    a("3. Read the elevation bands in the workbook: the river's area has a mean of %s ft and reaches %s ft, the creek's a "
      "mean of %s ft and a top of %s ft, so in a winter storm the two basins drain different shares of their area as "
      "rain." % (fmt(F["mean_elev_r"]), fmt(F["constants"]["zmax_r"]), fmt(F["mean_elev_c"]), fmt(F["constants"]["zmax_c"])))
    a("4. Measured the snow line's inputs: the storm lapse rate from ghcnd_tessel_daily_1950-2025.csv and "
      "ghcnd_durrow_ridge_daily_1950-2025.csv on days both caught 0.5 in or more (%.2f degrees C per kilometre, %s days; "
      "the SNOTEL pair gives %.2f), the rain-snow temperature from the two SNOTEL files (%.2f degrees C) and the rise of "
      "precipitation from the warm storms' ridge and valley totals (%d per cent per 1,000 ft)." % (
          F["lapse"], fmt(F["n_lapse"]), F["lapse_snotel"], F["t50"], F["g_pct"]))
    a("5. For each flood in the annual and above-base peak files, took the run of wet hours before its peak in "
      "lcd_tessel_field_hourly_1950-2025.csv (routine FM-15 reports; rain from the last wet hour within %d hours of the "
      "peak, dry spells of %d hours or less) and its rain-weighted temperature, the temperature the rain fell at (the "
      "reading at the river's peak hour is not: no rain fell in that hour in %d per cent of the floods, and it ran a median "
      "%.1f degrees C colder): %d floods were fed by rain, the river drained rain over a median %d per cent of its basin "
      "and the creek over %d per cent, and the river's own peaks follow that rain at a correlation of %.2f against %.2f "
      "for the storm's whole-basin rain." % (
          F["constants"]["lookback_hours"], F["constants"]["gap_hours"], F["dry_at_peak_pct"], F["peak_hour_colder_c"],
          F["n_matched"], F["share_river_median_pct"], F["share_creek_median_pct"], F["own_r"], F["total_rain_r"]))
    Vv = F["validation"]
    a("6. Checked the construction out of sample on the foothill gauge in usgs_%s_annual_peaks.txt (%d years, too short "
      "to carry under 7.4.3, a basin like the creek's): carried from the river's concurrent floods it reproduces the gauge's "
      "%d floods to a median %+d per cent (median absolute log error %.2f), where the drainage-area transfer runs %+d per "
      "cent, the standard atmosphere's lapse rate %+d per cent, rain without its rise with elevation %+d per cent, the "
      "valley's daily mean temperature %+d per cent and the airport's reading at the river's peak hour %+d per cent." % (
          F["val_site"], F["short_years"], Vv["golden"]["n"], Vv["golden"]["bias_pct"], Vv["golden"]["mad"],
          Vv["drainage_area"]["bias_pct"], Vv["lapse_6.5"]["bias_pct"], Vv["no_orography"]["bias_pct"],
          Vv["daily_peak_day"]["bias_pct"], Vv["peak_hour"]["bias_pct"]))
    a("7. Carried each flood to the creek at the ratio of the two basins' rain below its snow line with the state "
      "equation's drainage-area exponent, took the largest carried flood in each water year, and entered water year %s, "
      "with no flood fed by rain, as below the low-flood threshold." % " and ".join(str(y) for y in F["missing_years"]))
    a("8. Fitted Bulletin 17C to the carried series: the creek's 50 per cent flow is about %s cfs and its 1 per cent flow "
      "about %s cfs, and the two largest carried floods are water years %d and %d." % (
          fmt(F["q50_5000"]), fmt(F["q01_5000"]), top[0], top[1]))
    a("9. Compared the rated flows in hess_tm_durrow_creek_bridge_span_ratings.pdf with the curve: the 140 ft span's %s cfs "
      "would be exceeded %s, the %d ft span's %s cfs %s, so the county builds the %d ft span." % (
          fmt(sp[140]), F["bands"]["140"], call, fmt(sp[call]), F["bands"][str(call)], call))
    a("")
    a("No other conclusion survives. The drainage-area transfer, the region's mean unit flood (%s cfs) and the state "
      "equation (%s cfs, barred by section 7.4.3(c)) all assume the creek drains the same share of each storm as the high "
      "gauges, which the stations and the elevation bands refute. A snow line placed with the standard atmosphere's lapse "
      "rate (about %s cfs) or rain counted without its rise with elevation (about %s cfs) contradicts what the stations "
      "measure in storms and points to the 240 ft span; the foothill gauge's own floods reject each of these constructions and "
      "the drainage-area transfer, and its short record extended on the river's by MOVE.1 files %s cfs (the 140 ft span); "
      "the valley's daily mean temperature and the airport's reading at the "
      "river's peak hour both read air the rain did not fall in, which the rain-weighted hourly record separates, and every "
      "storm definition and rain weighting the hourly record allows keeps the 1 per cent flood at about %s cfs and the %d ft "
      "span." % (fmt(F["regional_unit_flood"]), fmt(F["regional_equation"]), fmt(V["lapse_6.5"]["q01_5000"]),
                 fmt(V["no_orography"]["q01_5000"]), fmt(F["sc_move1"]), fmt(F["q01_5000"]), call))
    a("")
    return "\n".join(lines)
