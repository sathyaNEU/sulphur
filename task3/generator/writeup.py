"""task3: submission.md, the four answer blocks, every figure from figures.json; each graded figure carries the band
the method's defensible variants span."""
import analysis as A


def _b(x, fmt="%.1f"):
    return (fmt + " to " + fmt) % (x[0], x[1])


def text(F):
    n = A.NAMES
    e, h, b, br, B = F["exp"], F["hind"], F["bridge"], F["bridge_range"], F["bands"]
    w1, w2 = F["call_keys"]
    rk = F["rank_keys"]
    rest = [k for k in rk if k not in F["call_keys"]]
    ro = F["route_exp"]
    V = F["variants_hind"]
    L = []
    a = L.append
    a("# task3 submission: Port Tolliver's FY2028 tide valves")
    a("")
    a("## Tags")
    a("")
    a("**Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (extreme-value and environmental-hazard "
      "analysis: tidal high-water exceedance carried from a tide gauge to low points with short records).")
    a("**Analytical objective:** Forecasting & Predictive Modeling.")
    a("")
    a("## Final Recommendation")
    a("")
    a("**Fund the valves at %s and %s.** They expect about %.1f and %.1f tidal flood days in the 2027-28 tide year against "
      "%.1f or fewer at each of the other three, and they come out on top under every defensible variant of the method; this "
      "rejects the pair that straight-line campaign transfers fund (%s and %s, %.1f and %.1f days), because Pellam Creek's "
      "high water bends below the line once the tide tops the marsh and River Road's only campaign sat in a wet late winter "
      "whose river lift the autumn king tides do not get."
      % (n[w1], n[w2], e[w1], e[w2], max(e[k] for k in rest), n["river"], n["marsh"],
         ro["river one offset"]["river"], ro["marsh straight line"]["marsh"]))
    a("")
    a("## Supplementary Questions")
    a("")
    a("### fy2028_tide_valve_ranking.xlsx")
    a("")
    a("1. A Ranking sheet with one row per low point, the funded two first, columns low point, LP ID, flooding elevation "
      "(ft NAVD88), 2025-26 tidal flood days, expected tidal flood days 2027-28 (one decimal), the 90 per cent range, funded "
      "(yes for %s and %s) and the basis; a Harbor gauge sheet; a Weather years sheet (each of the %d weather years' counts "
      "at every low point and that year's top two); a Variants sheet (the funded pair and each low point's expected days "
      "under each of the %d defensible variants); and a Routes sheet (the pair under each shortcut)."
      % (n[w1], n[w2], F["n_weather_years"], F["sweep_n"]))
    a("2. Expected tidal flood days in the 2027-28 tide year (the band each spans across the defensible variants): %s."
      % "; ".join("%s %.1f (%s)" % (n[k], e[k], _b(B["exp_" + k])) for k in A.ORDER))
    a("3. Tidal flood days in the 2025-26 tide year: %s."
      % "; ".join("%s %d (%s)" % (n[k], h[k], _b(B["hind_" + k], "%d")) for k in A.ORDER))
    a("4. %s and %s are the top two in %d of the %d weather years (%s across the variants); in the others River Road "
      "takes Front Street's place." % (n[w1], n[w2], F["pair_hold"], F["n_weather_years"], _b(B["pair_hold"], "%d")))
    a("5. The harbor gauge expects about %.1f days at its %.1f ft minor flood threshold in 2027-28 (%s across the variants), "
      "with a 90 per cent range of %d to %d days (low end %s, high end %s)."
      % (F["harbor_exp"], F["harbor_minor"], _b(B["harbor_exp"]), F["harbor_lo"], F["harbor_hi"], _b(B["harbor_lo"]),
         _b(B["harbor_hi"])))
    a("6. From %d days in 2025-26 to about %.1f in 2027-28 (a change of about %+.1f), sea level adds about %+.1f days "
      "(%+.1f to %+.1f whichever order the three changes are applied in); the tides and the weather share the rest, and "
      "their shares turn on the order: the tides between %+.1f and %+.1f and the weather between %+.1f and %+.1f (%+.1f and "
      "%+.1f averaged over the six orders), the three parts adding to the change in every order."
      % (F["harbor_2025"], F["harbor_exp"], b["total"], b["sea"], br["sea"][0], br["sea"][1], br["tides"][0],
         br["tides"][1], br["weather"][0], br["weather"][1], b["tides"], b["weather"]))
    a("")
    a("### fy2028_tide_valve_memo.pdf")
    a("")
    a("7. A one-page memo to the Stormwater Advisory Board that opens with the funded pair and its expected days, gives the "
      "five-row table and a bar chart of expected days with each low point's range (the funded two highlighted), then the "
      "harbor gauge's figures and change, and a paragraph each on how Front Street, Marsh and Oyster Creek Roads, and River "
      "Road were carried from the harbor.")
    a("")
    a("## Critical Components")
    a("")
    a("1. Marsh Road floods at a harbor high water of about **%.2f ft** (%.2f to %.2f across the bending forms), not the %.2f ft "
      "one straight line through its 2024 campaign gives, so it flooded on about **%d** days in 2025-26 (not %d) and expects "
      "about **%.1f** in 2027-28 (not %.1f)."
      % (F["marsh_Hstar"], min(F["marsh_variants"].values()), max(F["marsh_variants"].values()), F["marsh_Hlin"], h["marsh"],
         V["marsh_linear"], e["marsh"], ro["marsh straight line"]["marsh"]))
    a("2. River Road's high waters stand about **%.2f ft** higher at 25,000 cfs than at 5,000 cfs, and its campaign ran at "
      "%s cfs on average, so carried day by day on the Brayle's flows it flooded on about **%d** days in 2025-26 (%s across the "
      "flow forms the campaign fits; the campaign's single offset gives %d) and expects **%s** days in 2027-28 (%.1f by the "
      "best-fitting form), far below the single offset's %.1f."
      % (F["river_setup_25k"], "{:,}".format(F["river_q"][2]), h["river"], _b(B["hind_river"], "%d"), V["river_pooled"],
         _b(B["exp_river"]), e["river"], ro["river one offset"]["river"]))
    a("3. Front Street's lane sits at **%.2f ft NAVD88**, the lowest water level its street sensor records on the lane; it "
      "flooded on **%d** days in 2025-26, %d of them recorded by the sensor and %d in its outage."
      % (F["front_level_navd88"], h["front"], F["front_sensor_days"], F["front_outage_days"]))
    a("4. %s (**%.1f**) and %s (**%.1f**) lead the other three by at least **%.2f times** under every one of the %d "
      "defensible variants, and the pair holds in about **%d of %d** weather years."
      % (n[w1], e[w1], n[w2], e[w2], F["sweep_margin"], F["sweep_n"], F["pair_hold"], F["n_weather_years"]))
    a("")
    a("## Step-by-Step")
    a("")
    a("1. Put the harbor's verified high waters, predictions and monthly means (8673718 files) on the 1983-2001 MLLW datum "
      "and the inventory and loggers on NAVD88 with the datums page's %.2f ft; the 2025-26 tide year's mean sea level stood "
      "%.2f ft above the epoch's." % (F["datums_nav"], F["A25"]))
    a("2. Took each past high water's departure from its prediction less its tide year's mean sea level (an hourly residual "
      "swings through the tide, and the raw departure carries the sea level twice: %.1f days); replayed on 2025-26 it gives "
      "the observed %d days." % (F["harbor_raw_skew"], F["harbor_2025"]))
    a("3. Ran the 2027-28 predicted high waters at the planning sea level (%.2f ft) under each of the %d weather years: the "
      "harbor expects about %.1f days, %d to %d in nine years of ten; the count trend files %.1f and a Poisson range %d to %d."
      % (F["plan"], F["n_weather_years"], F["harbor_exp"], F["harbor_lo"], F["harbor_hi"], F["harbor_count_trend"],
         F["harbor_poisson"][0], F["harbor_poisson"][1]))
    a("4. Split the harbor's change from %d to %.1f over the six orders of applying sea level, tides and weather: about "
      "%+.1f, %+.1f and %+.1f; taken one at a time from 2025-26 the three do not add to the change."
      % (F["harbor_2025"], F["harbor_exp"], b["sea"], b["tides"], b["weather"]))
    a("5. Read Front Street's lane from the street sensor (pt-front-01): the lowest water level it records on the lane in "
      "readings that persist is %.2f ft NAVD88 (vehicles are single readings, rain ponds at lower tides); the drain rim in the "
      "inventory files %d days for 2025-26, and the sensor alone misses its outage's %d."
      % (F["front_level_navd88"], V["front_rim"], F["front_outage_days"]))
    a("6. Paired the 2024 Marsh Road campaign's (PEL-MR-24) high waters with the harbor's: one straight line fits the bulk but "
      "runs above all %d high waters where the harbor reached 8.3 ft or more (by %.2f ft on average), its residuals %.2f ft "
      "against %.2f for a transfer that bends near the marsh platform (4.29 ft NAVD88); the bending transfer floods the road "
      "at %.2f ft; Oyster Creek (OYS-CR-25) bends the same way and floods only at %.2f ft."
      % (F["marsh_top_n"], F["marsh_top_resid_abs"], F["marsh_sd"][1], F["marsh_sd"][0], F["marsh_Hstar"], F["oyster_Hstar"]))
    a("7. Paired River Road's campaign (HEN-RR-25) with the harbor and the USGS daily flows: the offset falls as the river "
      "falls (the staff checks rule out drift), and the linear, power and curved flow forms fit alike (the square-root and "
      "logarithmic forms fit worse), so the transfer carries the flow: 2025-26 gives about %d days and the single campaign "
      "offset %d." % (h["river"], V["river_pooled"]))
    a("8. Ran every low point through the same weather years, each with its own transfer and that year's river flows: %s; "
      "the funded pair is the same under all %d variants, and holds in about %d of the %d weather years."
      % ("; ".join("%s %.1f" % (n[k], e[k]) for k in rk), F["sweep_n"], F["pair_hold"], F["n_weather_years"]))
    a("")
    a("No other pair survives. Straight-line transfers fund River Road and Marsh Road (%.1f and %.1f days), but Marsh Road's "
      "own high waters above the marsh and River Road's own offset against the river's flow refute both; the drain rim and "
      "the untransferred harbor fund Front Street and River Road; the count trend and a Poisson range ignore the planning sea "
      "level and the clustering of tidal days. Every alignment of the weather years, every flow form the campaign fits and "
      "every bending form of the marsh transfer keep Wharf Street and Front Street on top."
      % (ro["river one offset"]["river"], ro["marsh straight line"]["marsh"]))
    a("")
    return "\n".join(L)
