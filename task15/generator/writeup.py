"""submission.md: the four answer blocks, every figure from figures.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FMT = ["Super", "Kvarter", "To Go"]


def k(x):
    return "{:,}".format(int(x))


def p1(x):
    return "%.1f" % x


def b(lo_hi, fmt=p1):
    return "%s to %s" % (fmt(lo_hi[0]), fmt(lo_hi[1]))


def write(F, workbook, note, task_dir=TASK):
    sv, rg, lic, bd = F["saving"], F["range"], F["licence"], F["bands"]
    ss, ws = F["sales_split"], F["waste_split"]
    c = F["careful"]["saving"]
    ce = F["competitor_effect_pct"]
    pil = list(F["pilot_opening_stores"])
    oth = [s for s in F["opening_stores"] if s not in pil]
    eff_txt = lambda xs: ", ".join("%s at %d" % (p1(ce[str(s)]), s) for s in sorted(xs, key=lambda s: ce[str(s)]))
    L = []
    a = L.append
    a("# task15 answer blocks")
    a("")
    a("## Tags")
    a("")
    a("**Domain:** Machine Learning Research, General Statistics & Data Science (benchmarking and ablations).")
    a("**Analytical objective:** Comparative Analysis & Explanation.")
    a("")
    a("## Final Recommendation")
    a("")
    a("**Switch the Super and Kvarter stores to Kornblomst's fresh forecast for 2027 and keep the To Go stores on AutoOrdre.** "
      "A Super store is expected to save %s DKK a year against its %s licence and a Kvarter store %s against %s, while a To Go "
      "store saves %s against %s; this rejects reading each format's saving off its own pilot stores with every sale before "
      "the last counted as demand, which gives Super %s, Kvarter %s and To Go %s and switches %s, because the forecast "
      "saves only in stores that trade through the weekend (the three To Go pilot stores are the format's high-street "
      "exceptions) and counting every sale overstates what the empty shelves turned away."
      % (k(sv["Super"]), k(lic["Super"]), k(sv["Kvarter"]), k(lic["Kvarter"]), k(sv["To Go"]), k(lic["To Go"]),
         k(c["Super"]), k(c["Kvarter"]), k(c["To Go"]), " and ".join(F["careful"]["switch"]) if F["careful"]["switch"] else "none"))
    a("")
    a("## Supplementary Questions")
    a("")
    a("### %s" % workbook)
    a("")
    a("1. The fresh sales growth gap, in percentage points of the pilot stores' fresh sales in the same weeks of 2025: the "
      "pilot stores' fresh sales grew %s per cent against %s per cent in the other stores, a gap of **%s** (%s), the "
      "difference of the two growth rates, split into:"
      % (p1(F["pilot_growth_pct"]), p1(F["other_growth_pct"]), p1(ss["gap"]), b(bd["gap_sales"])))
    a("   - Kornblomst's forecast at its recommended safety-stock setting, the sales the pilot stores' empty shelves turned "
      "away beyond their 2025 level carried by their format's change: **%s** (%s);" % (p1(ss["forecast"]), b(bd["sales_split"]["forecast"], lambda x: "%.2f" % x)))
    gS, gK, gT = (p1(F["growth_by_format_pct"][f]) for f in FMT)
    grew = ("%s per cent each" % gS) if gS == gK else ("%s and %s per cent" % (gS, gK))
    a("   - the pilot's format mix, more Super and Kvarter stores, whose fresh sales grew %s, and fewer To Go stores, "
      "which grew %s: **%s** (%s);" % (grew, gT, p1(ss["format_mix"]), b(bd["sales_split"]["format_mix"])))
    a("   - the discounter openings near pilot stores: **%s** (%s);" % (p1(ss["competitors"]), b(bd["sales_split"]["competitors"])))
    a("   - not explained by the three: %s." % p1(ss["rest"]))
    a("2. The fresh waste gap, in percentage points of the pilot stores' 2025 waste at cost: their waste fell %s per cent "
      "while the other stores' rose %s per cent, a gap of **%s** (%s), the difference of the two rates of change: "
      "Kornblomst's forecast at its recommended setting "
      "**%s** (%s), the format mix "
      "**%s** (%s), the discounter openings **%s** (%s), not explained %s."
      % (p1(F["pilot_waste_fall_pct"]), p1(F["other_waste_change_pct"]), p1(ws["gap"]), b(bd["gap_waste"]),
         p1(ws["forecast"]), b(bd["waste_split"]["forecast"]), p1(ws["format_mix"]), b(bd["waste_split"]["format_mix"]),
         p1(ws["competitors"]), b(bd["waste_split"]["competitors"]), p1(ws["rest"])))
    a("3. Each format's expected saving per store and year from switching, DKK excluding VAT, as agreement FK-2026-014 "
      "defines it (4.2 and 4.3): Super **%s** (%s); Kvarter **%s** (%s); To Go **%s** (%s)."
      % (k(sv["Super"]), b(bd["saving"]["Super"], k), k(sv["Kvarter"]), b(bd["saving"]["Kvarter"], k), k(sv["To Go"]),
         b(bd["saving"]["To Go"], k)))
    a("4. The 80 per cent range on each, DKK: Super **%s to %s**; Kvarter **%s to %s**; To Go **%s to %s**. Each end lands "
      "in its band under any sound resampling of the stores: Super %s and %s; Kvarter %s and %s; To Go %s and %s."
      % (k(rg["Super"][0]), k(rg["Super"][1]), k(rg["Kvarter"][0]), k(rg["Kvarter"][1]), k(rg["To Go"][0]), k(rg["To Go"][1]),
         b(bd["range"]["Super_lo"], k), b(bd["range"]["Super_hi"], k), b(bd["range"]["Kvarter_lo"], k),
         b(bd["range"]["Kvarter_hi"], k), b(bd["range"]["To Go_lo"], k), b(bd["range"]["To Go_hi"], k)))
    a("5. The formats to switch: Super and Kvarter, %s and %s a store above their licences; To Go stays on AutoOrdre, %s "
      "against its licence." % (k(F["margin_over_licence"]["Super"]), k(F["margin_over_licence"]["Kvarter"]),
                                 k(F["margin_over_licence"]["To Go"])))
    a("6. The workbook opens on a Decision sheet with one row per format (stores, commuter-week stores, pilot stores, expected "
      "saving, the range's two ends, licence, saving less licence, switch or stay), then: Gap causes (the two gaps with "
      "their parts); Stores (all %s stores with format, pilot flag, 2025 weekend share of fresh units, trading week, 2025 "
      "fresh sales and waste, and the waste part, margin part and expected saving per year); Pilot stores (each pilot "
      "store's expected and actual waste, waste saving, margin change and 26-week saving, and the rates by trading week); "
      "Empty shelves (units turned away by group and period, and the check on the days the shelf did not run out); "
      "Openings; Routes (each shortcut's three savings and the formats it would switch); Notes." % F["n_stores_total"])
    a("")
    a("### %s" % note)
    a("")
    a("7. Four slides: the call, with one chart of each format's expected saving (dot) and its 80 per cent range (bar) "
      "against its licence (tick) beside the three savings and ranges; why the formats differ (the trading week, with the "
      "two rates and the shadow forecasts' weekend ratio, and the high-street To Go pilot stores); the two gaps and their "
      "parts in one table; the units turned away, with a table of what each way of reading the pilot gives and the formats "
      "it would switch.")
    a("")
    a("## Critical Components")
    a("")
    a("1. Empty shelves turned away about **%s** fresh units in the pilot stores over the pilot weeks (%s) against **%s** in "
      "the same weeks of 2025 (%s): each sold-out day's demand from its sales before the last sale and the share of the "
      "day's trade the hourly profile puts before that time, counting one sale fewer than the day made."
      % (k(F["lost_units"]["pilot_2026"]), b(bd["lost_units"]["pilot_2026"], k), k(F["lost_units"]["pilot_2025"]),
         b(bd["lost_units"]["pilot_2025"], k)))
    a("2. On the %s store-item days the shelf did not run out with two or more sales, where the day's demand is what sold, "
      "counting every sale overstates the day's sales by **%s per cent** (%s), %s per cent on days with six sales or fewer; "
      "one sale fewer is within %s per cent."
      % (k(F["check_days"]), p1(F["check_plain_over_pct"]), b(bd["check_plain_over"]), p1(F["check_plain_over_small_pct"]),
         p1(F["check_os_over_pct"])))
    a("3. The saving follows a store's trading week, not its format: weekend-trading pilot stores avoided **%s per cent** of "
      "the fresh waste they would have written off (%s) and commuter-week pilot stores **%s per cent** (%s), because "
      "Kornblomst's chain-wide model weights a commuter-week store's weekend about %.1f times as heavily as the store's "
      "own week does (%.1f to %.1f however the stores are pooled) and a weekend-trading store's about as heavily (%.2f to "
      "%.1f); the To Go stores in the pilot all trade through the weekend, while most To Go stores trade a commuter week."
      % (p1(F["waste_rate_pct"]["weekend"]), b(bd["waste_rate"]["weekend"]), p1(F["waste_rate_pct"]["commuter"]),
         b(bd["waste_rate"]["commuter"]), F["shadow_ratio"]["commuter"], F["shadow_ratio_range"]["commuter"][0],
         F["shadow_ratio_range"]["commuter"][1], F["shadow_ratio_range"]["weekend"][0], F["shadow_ratio_range"]["weekend"][1]))
    a("4. The discounter openings, read from each store's ambient weekly sales against the same weeks of 2025 and its "
      "format's stores with no opening, took (per cent of trade, each within 2 points) %s among the pilot stores, and %s "
      "elsewhere." % (eff_txt(pil), eff_txt(oth)))
    a("")
    a("## Step-by-Step")
    a("")
    a("1. Conformed `dagssalg_frisk_2025.csv` (semicolons, decimal commas, Windows-1252) and `dagssalg_frisk_2026.csv` to "
      "one store, item and day record: the export job's %s re-sent rows dropped from the 2025 file, the two dairy items renumbered on 1 January 2026 "
      "joined through the former numbers in `vareregister_frisk.xlsx`, the pilot stores taken from the order basis in "
      "`ordreforslag_2026.csv` (Annex 1 of `pilotaftale_kornblomst_2026.pdf`). Over ISO weeks %d to %d of 2026 against "
      "the same weeks of 2025 the pilot stores' fresh sales grew %s per cent against %s, and their waste at cost fell %s per "
      "cent while the other stores' rose %s: gaps of %s and %s points, as `pilot_dashboard_uge35.xlsx` shows."
      % (k(F["duplicate_rows_2025"]), F["pilot_weeks"][0], F["pilot_weeks"][1], p1(F["pilot_growth_pct"]),
         p1(F["other_growth_pct"]), p1(F["pilot_waste_fall_pct"]), p1(F["other_waste_change_pct"]), p1(ss["gap"]),
         p1(ws["gap"])))
    a("2. Read as the saving, the dashboard says every store saves %s per cent of its waste: Super %s, Kvarter %s, To Go %s "
      "a store, every format switched (the quick reading). It leaves out the margin the forecast's empty shelves cost, and "
      "the gap carries the openings and the format mix."
      % (p1(F["quick"]["dashboard_rate_pct"]), k(F["quick"]["saving"]["Super"]), k(F["quick"]["saving"]["Kvarter"]),
         k(F["quick"]["saving"]["To Go"])))
    a("3. A day sold out when its closing stock is zero. Its demand is the sales made before the last sale over the share of "
      "the day's trade `timeprofil_salg_frisk.csv` puts before that time (format, category and weekday), counting one sale "
      "fewer than made, since the last sale is the S-th of the day's D customers and falls on average at S/(D+1) of the "
      "day's trade: %s units turned away in the pilot stores in the pilot weeks and %s in 2025 (%s and %s per cent of "
      "demand). Counting every sale gives %s and %s (the careful but hurried reading; how the profile is interpolated "
      "inside the hour moves either by up to %d per cent)."
      % (k(F["lost_units"]["pilot_2026"]), k(F["lost_units"]["pilot_2025"]), p1(F["lost_share_pilot_2026_pct"]),
         p1(F["lost_share_pilot_2025_pct"]), k(F["lost_units_plain"]["pilot_2026"]), k(F["lost_units_plain"]["pilot_2025"]),
         F["plain_interp_spread_pct"]))
    a("4. Checked both forms where the day's demand is known, on the %s store-item days the shelf did not run out with two "
      "or more sales: counting every sale overstates the day's sales by %s per cent (%s on days with six sales or fewer), "
      "one sale fewer by %s (%s)."
      % (k(F["check_days"]), p1(F["check_plain_over_pct"]), p1(F["check_plain_over_small_pct"]), p1(F["check_os_over_pct"]),
         p1(F["check_os_over_small_pct"])))
    a("5. Read the openings in `konkurrentaabninger.csv` off the ambient (Kolonial) rows of `bi_uge_butik_kategori.csv`, which "
      "fresh ordering never touches (category codes renamed from 2026-W02): each week of 2026 against the same week of 2025 "
      "and against the format's stores with no opening, the step across the opening date after a four-week ramp, %s among "
      "the pilot stores and %s elsewhere." % (eff_txt(pil), eff_txt(oth)))
    a("6. Split the sales gap: the formats' own growth in their AutoOrdre stores with no opening (Super %s, Kvarter %s, To Go "
      "%s per cent) on each group's 2025 format mix gives %s; the openings' share of trade, 2026 against 2025, %s; the pilot "
      "stores' sales turned away beyond their 2025 level carried by their format's change, %s; %s is left. Taking all that "
      "is left after the openings and the mix as the forecast gives %s, inside the band. The waste gap the same way: "
      "forecast %s, mix %s, openings %s, %s left."
      % (p1(F["growth_by_format_pct"]["Super"]), p1(F["growth_by_format_pct"]["Kvarter"]), p1(F["growth_by_format_pct"]["To Go"]),
         p1(ss["format_mix"]), p1(ss["competitors"]), p1(ss["forecast"]), p1(ss["rest"]), p1(F["sales_split_residual_forecast"]),
         p1(ws["forecast"]), p1(ws["format_mix"]), p1(ws["competitors"]), p1(ws["rest"])))
    a("7. Each pilot store's 26-week saving (4.2): its 2025 waste carried by its format's change in the AutoOrdre stores "
      "with no opening and by the trade an opening took, less what it wrote off, plus the change in margin on the units its "
      "shelves turned away against the same expectation. Reading each format's rate off its own pilot stores (Super %s, "
      "Kvarter %s, To Go %s per cent of waste) with every sale counted is the careful but hurried reading: Super %s, "
      "Kvarter %s, To Go %s, switching %s."
      % (p1(F["careful_waste_rate_by_format_pct"]["Super"]), p1(F["careful_waste_rate_by_format_pct"]["Kvarter"]),
         p1(F["careful_waste_rate_by_format_pct"]["To Go"]), k(c["Super"]), k(c["Kvarter"]), k(c["To Go"]),
         " and ".join(F["careful"]["switch"]) if F["careful"]["switch"] else "none"))
    a("8. The pilot stores' savings follow their weekend share, not their format. The 2025 weekend share of each store's "
      "fresh units splits the stores at its widest gap (%.2f): weekend-trading pilot stores saved %s per cent of their "
      "waste, the commuter-week ones (all Kvarter) %s. The shadow forecasts in `ordreforslag_2026.csv` show why: "
      "Kornblomst's weekend-to-weekday ratio, as a multiple of AutoOrdre's (which reads each store's own week), averages "
      "%.2f over the commuter-week stores and %.2f over the weekend-trading ones (%.1f to %.1f and %.2f to %.1f however the "
      "stores are pooled). Most To Go stores trade a commuter week; the pilot's To Go stores are high-street stores that do "
      "not."
      % (F["weekend_cut"], p1(F["waste_rate_pct"]["weekend"]), p1(F["waste_rate_pct"]["commuter"]),
         F["shadow_ratio"]["commuter"], F["shadow_ratio"]["weekend"], F["shadow_ratio_range"]["commuter"][0],
         F["shadow_ratio_range"]["commuter"][1], F["shadow_ratio_range"]["weekend"][0], F["shadow_ratio_range"]["weekend"][1]))
    a("9. Carried every store by its own trading week (4.3): the waste part at its type's rate on the store's 2025 waste, "
      "the margin part at %.2f or %.2f per cent of its 2025 fresh sales, twice the 26 weeks, averaged over each format's "
      "stores: Super %s, Kvarter %s, To Go %s. Two conventions carry this: the pilot stores' rates are pooled by trading "
      "week across formats (taken format by format within the trading week they give Super %s, Kvarter %s and To Go %s, "
      "inside every band), and the margin part is read from the units the empty shelves turned away, not from the recorded "
      "gross margin."
      % (F["margin_rate_pct"]["weekend"], F["margin_rate_pct"]["commuter"], k(sv["Super"]), k(sv["Kvarter"]), k(sv["To Go"]),
         k(F["rivals"]["unc_fxt"]["saving"]["Super"]), k(F["rivals"]["unc_fxt"]["saving"]["Kvarter"]),
         k(F["rivals"]["unc_fxt"]["saving"]["To Go"])))
    a("10. Ranged by %s resamples of the stores, the pilot stores within their trading week and the others within their "
      "format, every step redone: the 80 per cent ranges in answer 4." % k(F["resamples"]))
    a("")
    rc = F["recorded_route_spread"]["Super"]
    sh = F["weekend_pilot_saving_share"]
    R_ = F["routes"]
    sw = lambda x: "none" if not x else (x[0] if len(x) == 1 else ", ".join(x[:-1]) + " and " + x[-1])
    a("No other conclusion survives, and each of four separate ways of going wrong lands on a wrong set by itself. Counting every "
      "sale before the last as a sold-out day's demand (refuted by the in-stock days) keeps Super off even by trading "
      "week (%s against %s): it switches %s. Reading each format off its own pilot stores switches To Go (%s against %s), "
      "because To Go's high-street pilot stores stand for commuter-week stores the forecast costs money: it switches %s. "
      "Carrying the whole saving on fresh sales keeps Kvarter off (%s against %s): it switches %s, and it does not fit the "
      "pilot, where the weekend-trading stores saved %.2f, %.2f and %.2f per cent of their fresh sales in Super, Kvarter and "
      "To Go, because waste avoided is a share of waste and a Super store writes off %s per cent of its fresh sales against "
      "%s for a Kvarter store (carrying it all on waste instead, Kvarter %s, fails the other way: the weekend-trading Super "
      "pilot stores gave up %s times the margin of the Kvarter ones with %s times their fresh sales and %s times their "
      "waste). Reading the margin part off the recorded gross margin is not agreement 4.2's out-of-stock sales: it books "
      "to the forecast every other movement in a store's margin (store %d's recorded margin ran %s below its format's over "
      "the 26 weeks while its turned-away units account for %s of that), spreads %s DKK a Super store over the 26 weeks on "
      "the stores that kept AutoOrdre against %s for units turned away, and puts Super at %s pooled by trading week and %s "
      "format by format: it switches %s. The dashboard's waste gap, read as the saving, leaves out the margin and carries "
      "the openings and the mix: it switches %s."
      % (k(R_["plain_type"]["saving"]["Super"]), k(F["licence"]["Super"]), sw(R_["plain_type"]["switch"]),
         k(R_["by_format"]["saving"]["To Go"]), k(F["licence"]["To Go"]), sw(R_["by_format"]["switch"]),
         k(R_["single_sales_type"]["saving"]["Kvarter"]), k(F["licence"]["Kvarter"]), sw(R_["single_sales_type"]["switch"]),
         sh["Super"]["of_sales_pct"], sh["Kvarter"]["of_sales_pct"], sh["To Go"]["of_sales_pct"],
         p1(F["waste_to_sales_2025_pct"]["Super"]), p1(F["waste_to_sales_2025_pct"]["Kvarter"]),
         k(R_["single_waste_type"]["saving"]["Kvarter"]), p1(F["weekend_pilot_super_over_kvarter"]["margin"]),
         p1(F["weekend_pilot_super_over_kvarter"]["sales"]), p1(F["weekend_pilot_super_over_kvarter"]["waste"]),
         F["store_2158_margin_shortfall"]["store"], k(F["store_2158_margin_shortfall"]["recorded"]),
         k(F["store_2158_margin_shortfall"]["turned_away"]), k(rc["recorded_sd"]), k(rc["turned_away_sd"]),
         k(R_["recorded_type"]["saving"]["Super"]), k(R_["recorded_fxt"]["saving"]["Super"]), sw(R_["recorded_type"]["switch"]),
         sw(F["quick"]["switch"])))
    a("")
    txt = "\n".join(L)
    open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8").write(txt)
    return txt


if __name__ == "__main__":
    F = json.load(open(os.path.join(HERE, "figures.json")))
    import deliver as D
    print(write(F, D.WORKBOOK, D.NOTE))
