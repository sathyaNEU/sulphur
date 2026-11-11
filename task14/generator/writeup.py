"""task14: submission.md, the four answer blocks, written from figures.json (no figure is typed here)."""
import measure as MS

NAMES = {"NAT": "Penmarra", "HC": "Hallam Central", "HN": "Hallam North", "HE": "Hallam East", "HS": "Hallam South",
         "KC": "Kerrow Coast", "MV": "Midvale", "WS": "Westerly"}
CAREFUL_SHORT = {
    "the panel's rises carried to every landlord": "carrying the rent survey's rises to every landlord",
    "the latest recorded rent carried forward at the panel's rate": "carrying each tenancy's latest recorded rent "
                                                                    "forward at the survey's rate",
    "the recorded rent where an additional bond exists, the model otherwise": "taking the recorded rent wherever an "
                                                                              "additional bond exists",
}
VARIANT_KEYS = list(CAREFUL_SHORT)


def f1(x):
    return "%.1f" % x


def f2(x):
    return "%.2f" % x


def n0(x):
    return "{:,}".format(int(x))


def regions(d, fmt=f1):
    return ", ".join("%s %s" % (NAMES[g], fmt(d[g])) for g in MS.REGIONS)


def write(F, path, workbook, slides):
    b = F["bands"]
    lo, hi = F["dec26_range"]
    sp = F["slow_pts"]
    ser = F["series"]
    qs = list(ser.keys())
    vs, vd, vr = F["variants_sep26"], F["variants_dec26"], F["variants_relet_change"]
    survey_all, carry_fwd, hybrid = VARIANT_KEYS
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Other, Survey Research & Official Statistics (seasonal adjustment and official time-series "
               "production).  \n**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).\n")
    out.append("## Final Recommendation\n")
    out.append("**Expect the bond-based measure to show private rents up %s per cent in the year to the December 2026 "
               "quarter (90 per cent range %s to %s), down from %s in the year to September 2026**, because the "
               "build-to-rent landlord %s, which reviews every 1 December and is not yet on file, will raise its rents "
               "%s per cent (the September CPI plus %s) against %s a year earlier, landlord %s's 1 November review is "
               "%s against %s, and going rents have eased since July. Reject the %s that carrying September forward gives, the %s of a straight trend through "
               "the quarters, and the %s that %s and reading the register as it stands on 31 December gives.\n"
               % (f1(F["dec26"]["NAT"]), f1(lo), f1(hi), f1(F["sep26"]["NAT"]), F["a_landlord"],
                  f1(F["a_review_2026"]), f1(F["a_margin"]), f1(F["a_review"]["2025"]), F["b_landlord"],
                  f1(F["b_review_2026"]), f1(F["b_review"]["2025"]),
                  f1(F["carry_dec26"]), f1(F["trend_dec26"]), f1(F["careful_dec26"]),
                  CAREFUL_SHORT[F["careful_name"]]))
    out.append("## Supplementary Questions\n")
    out.append("### %s\n" % workbook)
    out.append("1. A \"Measure\" sheet with one row per quarter from 2022Q1 to 2026Q3 and a projected 2026Q4 row; the "
               "national annual change in per cent, each quarter within %s point: %s. The September 2026 quarter by "
               "region, each within %s point (Penmarra %s, within %s): %s."
               % (b["series"], "; ".join("%s %s" % (q, f1(ser[q])) for q in qs), b["region"],
                  f1(F["sep26"]["NAT"]), b["national"], regions(F["sep26"])))
    out.append("2. Bonded tenancies in place on 30 September 2026 (a \"Year to Sep 2026\" sheet, one row per region and a "
               "Penmarra row), each within %s per cent: Penmarra %s; %s." % (b["held_pct"], n0(F["held"]["NAT"]),
                                                                            regions(F["held"], n0)))
    out.append("3. Dwellings re-let in the year to 30 September 2026, beside the tenancies in place, each within %s per "
               "cent: Penmarra %s; %s." % (b["relet_pct"], n0(F["relet_n"]["NAT"]), regions(F["relet_n"], n0)))
    out.append("4. Continuing tenancies, year to September 2026: rent payable up %s per cent (within %s point), with %s "
               "per cent of them seeing a rise (within %s points; the survey's share of anniversaries with a rise, by "
               "year and region, for small landlords' tenancies, and the operators' recorded reviews for theirs)."
               % (f1(F["cont_change"]), b["change_pts"], f1(F["cont_share"]), b["share_pts"]))
    out.append("5. Dwellings re-let: rent up %s per cent on what the earlier tenancies were paying on 30 September "
               "2025 (within %s point)." % (f1(F["relet_change"]), b["relet_change"]))
    out.append("\n### %s\n" % slides)
    out.append("6. Three slides. The first gives the December 2026 figure for Penmarra, %s per cent (within %s point), "
               "with its 90 per cent range of %s to %s (each end within %s point, a half-width between %s and %s "
               "point), and a bar chart of the regions, each within %s point: %s. The second charts the national "
               "measure from 2022Q1 with the projected December point."
               % (f1(F["dec26"]["NAT"]), b["dec_national"], f1(lo), f1(hi), b["range_end"], b["half_lo"],
                  b["half_hi"], b["dec_region"], regions(F["dec26"])))
    out.append("7. The third slide splits the change from %s per cent in the year to September 2026 to %s in the year "
               "to December between the two groups: a fall of %s points (within %s), of which continuing tenancies %s "
               "and re-lettings %s (each within %s point), each group's contribution to the measure in both (%s and "
               "%s points to September, %s and %s to December), with the year to September by group (answers 4 and "
               "5)." % (f1(F["sep26"]["NAT"]), f1(F["dec26"]["NAT"]), f2(sp["fall"]), b["fall"], f2(sp["continuing"]),
                        f2(sp["relet"]), b["contrib"], f2(F["contrib26"]["continuing"]), f2(F["contrib26"]["relet"]),
                        f2(F["contrib_dec"]["continuing"]), f2(F["contrib_dec"]["relet"])))
    out.append("\n## Critical Components\n")
    out.append("1. The national measure for the year to September 2026 is **%s per cent** (Hallam Central **%s**, "
               "Midvale **%s**), every quarter back to 2022Q1 on the same footing, with a peak of **%s** in %s."
               % (f1(F["sep26"]["NAT"]), f1(F["sep26"]["HC"]), f1(F["sep26"]["MV"]), f1(F["peak"]), F["peak_q"]))
    out.append("2. Continuing tenancies' rent payable rose **%s per cent**, with **%s per cent** of them seeing a rise; "
               "the register's additional bonds show a rise for only **%s per cent**, while the block operators' own "
               "bonds record every review they make." % (f1(F["cont_change"]), f1(F["cont_share"]),
                                                          f1(F["topup_share"])))
    out.append("3. **%s** dwellings were re-let in the year, their rent up **%s per cent** on what the earlier "
               "tenancies were paying; tying re-lettings by property identifier alone finds **%s**."
               % (n0(F["relet_n"]["NAT"]), f1(F["relet_change"]), n0(F["pid_relet_n"])))
    out.append("4. Of the **%s**-point fall from the year to September to the year to December, continuing "
               "tenancies account for **%s** point and re-lettings **%s**." % (f2(sp["fall"]), f2(sp["continuing"]),
                                                                              f2(sp["relet"])))
    out.append("\n## Step-by-Step\n")
    st = []
    st.append("Conformed the register from tbb_legacy_register_extract_2023-03-05.csv and "
              "tbb_bond_events_2023-03-06_to_2026-11-27.csv: re-sent legacy rows dropped, each migrated bond joined to "
              "its legacy record by legacy_bond_no, rents made weekly (PS-2026-07 2.3), extra-zero rents found against "
              "their bond amounts, landlords followed through tbb_landlord_id_crosswalk_2023-03-06.csv and regions "
              "taken from pso_suburb_region_concordance_2024.csv; a tenancy covers each day from its start until its "
              "refund or the next tenancy's start (2.2): %s held on 30 September 2026." % n0(F["held"]["NAT"]))
    st.append("Found each tenancy's dwelling: the property identifier where the bond has one (bonds with different "
              "identifiers are different dwellings, 2.1), otherwise the premises text parsed to unit, number and "
              "street and matched to the validated address of a later lodgement in the same postcode (a one-letter "
              "street slip or a reversed unit and number allowed): %s dwellings re-let in the year to September 2026. "
              "Joining on the property identifier alone finds %s, because every bond migrated in March 2023 lacks one "
              "and those are the longest tenancies with the largest catch-up; identical address strings alone find %s."
              % (n0(F["relet_n"]["NAT"]), n0(F["pid_relet_n"]), n0(F["exact_relet_n"])))
    vd = F["validation"]["2026"]
    vg = F["validation_gap"]["2026"]
    st.append("Measured continuing tenancies' rises on pso_rent_survey_2018q1_2026q3.csv: %s anniversaries with the "
              "rent reported either side, design-weighted by year and region, carried from each tenancy's starting "
              "rent. The additional bonds show a rise for %s per cent of continuing tenancies where the survey's rates "
              "put it at %s per cent for the same tenancies, so a missing additional bond is not a record of no rise. "
              "Tied to the register by address (%s of the survey's %s dwellings), the survey's anniversaries with an "
              "additional bond lodged rose %s per cent in 2025 against %s without and %s overall, so the rises the "
              "bonds record are the larger ones. Checked on the %s small-landlord tenancies both sources held on the "
              "survey's August 2026 reference day, the rents carried from each starting rent come within %s per cent "
              "of the rents the survey reports, the recorded rents fall %s per cent short, the latest recorded rent "
              "carried forward at the survey's rate overshoots by %s per cent and the recorded rent wherever a bond "
              "exists falls %s per cent short. The block operators lodge an additional bond at every review and the "
              "survey, drawn from dwellings let at the end of 2017, holds none of their blocks, so their rents come "
              "from their own bonds. Carrying the survey's rises to every landlord gives %s per cent for September; "
              "carrying each tenancy's latest recorded rent forward gives %s for September but runs up to 0.3 point "
              "high through 2023 and 2024 and puts the re-letting rise at %s."
              % (n0(F["panel_pairs"]), f1(F["topup_share"]), f1(F["survey_share"]), n0(F["panel_link"]["linked"]),
                 n0(F["panel_link"]["dwellings"]), f1(F["panel_link"]["years"]["2025"]["with"]),
                 f1(F["panel_link"]["years"]["2025"]["without"]), f1(F["panel_link"]["years"]["2025"]["all"]),
                 n0(vd["n"]), f1(vg["model"]), f1(vg["recorded_short"]), f1(vg["carry_over"]), f1(vg["hybrid_short"]),
                 f1(vs[survey_all]), f1(vs[carry_fwd]), f1(vr[carry_fwd])))
    st.append("Priced each re-letting against what the earlier tenancy was paying on 30 September 2025 (2.4): up %s "
              "per cent; against the earlier starting rent it reads %s, counting the earlier tenancy's own rises "
              "twice." % (f1(F["relet_change"]), f1(F["relet_start_change"])))
    st.append("Computed the measure for every quarter: %s per cent in the year to September 2026, from a peak of %s "
              "in %s; reading the additional bonds as every rise gives %s, and property identifiers alone %s."
              % (f1(F["sep26"]["NAT"]), f1(F["peak"]), F["peak_q"], f1(F["topups_sep26"]), f1(F["pid_sep26"])))
    tb, pb = F["trend_bt_err"], F["proj_bt_err"]
    rp, rs = F["reviews_part"], F["rest_part"]
    st.append("Projected 31 December 2026 from the register as it stood on 27 November, each tenancy carried at the "
              "rates the same weeks of 2023 to 2025 showed when the register is read as it stood on their own 27 "
              "November (by age and landlord class), with December re-lettings at going rents from the register's "
              "repeat-letting index: landlord %s's 1 November review (%s per cent on the %s bonds lodged) completed "
              "for its %s eligible tenancies not yet on file, and landlord %s's 1 December review applied to %s "
              "tenancies at %s per cent, its rule read off its earlier reviews (%s, %s and %s in 2023 to 2025, each "
              "the September CPI in pso_cpi_2026q3.xlsx plus %s): %s per cent nationally; %s. The same projection "
              "missed December 2023, 2024 and 2025 by %s, %s and %s point; a straight trend through the quarters "
              "missed them by %s, %s and %s and gives %s now. Read as it stands on 31 December the register gives %s; "
              "on the earlier Decembers that reading fell short by %s, %s and %s, of which the reviews not yet on file "
              "were %s, %s and %s and the December re-lettings %s, %s and %s, and in 2026 the reviews still add %s but "
              "the re-lettings only %s: about %s tenancies end between 27 November and 31 December, %s of them re-let, "
              "and %s of the %s dwellings empty on the cut day let again, at going rents %s per cent above the rents "
              "they replace against %s and %s in 2024 and 2025, as the register's repeat-letting index eased. "
              "Correcting the register as it stands by its past errors gives %s; reading it on 27 November (%s) and "
              "adding the earlier years' change to December gives %s, and missed December 2024 by %s point, because "
              "both parts of that change shrink in 2026."
              % (F["b_landlord"], f1(F["b_review_2026"]), n0(F["reviewed_onfile_n"]), n0(F["pending_n"]),
                 F["a_landlord"], n0(F["scheduled_n"]), f1(F["a_review_2026"]), f1(F["a_review"]["2023"]),
                 f1(F["a_review"]["2024"]), f1(F["a_review"]["2025"]), f1(F["a_margin"]), f1(F["dec26"]["NAT"]),
                 regions(F["dec26"]), f1(abs(pb[0])), f1(abs(pb[1])), f1(abs(pb[2])), f1(abs(tb[0])), f1(abs(tb[1])),
                 f1(abs(tb[2])), f1(F["trend_dec26"]), f1(F["asstands_dec26"]),
                 f2(F["asstands_short"][0]), f2(F["asstands_short"][1]), f2(F["asstands_short"][2]), f2(rp[0]),
                 f2(rp[1]), f2(rp[2]), f2(rs[0]), f2(rs[1]), f2(rs[2]), f2(rp[3]), f2(F["rest_part_2026"]),
                 n0(F["dec_churn"]["2026"]["ending"]), n0(F["dec_churn"]["2026"]["relet"]),
                 n0(F["dec_churn"]["2026"]["let_from_empty"]), n0(F["dec_churn"]["2026"]["empty"]),
                 f1(F["dec_churn"]["2026"]["margin"]), f1(F["dec_churn"]["2024"]["margin"]),
                 f1(F["dec_churn"]["2025"]["margin"]), f1(F["asstands_adj_dec26"]), f1(F["analog"]["nov26"]),
                 f1(F["analog"]["dec26"]), f2(F["analog"]["max_error"])))
    st.append("Split the change from %s to %s into each group's contribution to the measure (its change in rent over "
              "the whole base) in the two years: continuing tenancies %s point, re-lettings %s (%s together)."
              % (f1(F["sep26"]["NAT"]), f1(F["dec26"]["NAT"]), f2(sp["continuing"]), f2(sp["relet"]),
                 f2(sp["fall"])))
    bt = F["backtest"]
    st.append("Set the 90 per cent range from the survey resampled by dwelling within its strata (%s draws) and the "
              "same projection's error on December 2023, 2024 and 2025 (projected %s, %s and %s against %s, %s and "
              "%s): %s to %s." % (n0(F["boot_n"]), f1(bt[0]["projected"]), f1(bt[1]["projected"]),
                                  f1(bt[2]["projected"]), f1(bt[0]["actual"]), f1(bt[1]["actual"]),
                                  f1(bt[2]["actual"]), f1(lo), f1(hi)))
    for i, s in enumerate(st, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("No other December figure survives. Carrying September forward (%s) and a trend through the quarters "
               "(%s) cannot see the two operator reviews that fall after September, each about half the one it "
               "replaces, which is why the trend's errors on earlier Decembers (up to %s point) double now; the "
               "register read as it stands (%s) leaves out the review not yet on file and every December re-letting, "
               "and correcting it by its past errors (%s), or adding the earlier years' change to the 27 November "
               "reading (%s), borrows a re-letting premium the easing market no longer pays. For September, the additional bonds read as every rise (%s), property identifiers alone (%s), "
               "the earlier starting rent (%s), the survey's rises given to the operators (%s) and recorded rents "
               "carried forward at the survey's rate (re-letting rise %s) each fail on a fact the files show: the "
               "survey's rises with no bond lodged, the migrated bonds' missing identifiers, 2.4's rent on the earlier "
               "day, the operators' complete records, and the recorded rises being the larger ones, which the "
               "survey's own reported rents confirm."
               % (f1(F["carry_dec26"]), f1(F["trend_dec26"]), f1(max(abs(x) for x in F["trend_bt_err"])),
                  f1(F["asstands_dec26"]), f1(F["asstands_adj_dec26"]), f1(F["analog"]["dec26"]),
                  f1(F["topups_sep26"]), f1(F["pid_sep26"]),
                  f1(F["start_sep26"]), f1(vs[survey_all]), f1(vr[carry_fwd])))
    open(path, "w").write("\n".join(out) + "\n")
