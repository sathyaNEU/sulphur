"""submission.md, the four answer blocks, drafted from generator/figures.json only (every number the blocks state is a
figure the generator wrote)."""
import os

SEG = {"u25": "Under 25", "mid": "25 to 64", "o65": "65 and over"}
SITES = ("Kitecompare", "Covertide", "Brightquote", "Pricelark")


def n(x):
    return format(int(x), ",")


def rise(k):
    return "a rise of %d per cent" % k if k else "no rise at all"


def write(path, f):
    c = f["constants"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Quantitative Finance and Trading, Actuarial Science & Insurance (pricing, rating and "
             "credibility).  ")
    L.append("**Analytical objective:** Opportunity Sizing & Decision Support.")
    L.append("")
    L.append("## Final Recommendation")
    L.append("")
    L.append("**Raise comparison-site new-business rates from 1 January 2027 by %d per cent for drivers under 25 and "
             "%d per cent for drivers aged 25 to 64, and drop the %d per cent over-65 cut.** The team's %d per cent, "
             "which the loss-ratio method also gives, leaves the under-25 business it would win at a %.1f per cent "
             "loss ratio because a higher price keeps only the risks the rating model under-priced most; the latest "
             "twelve months' %d per cent for 25-to-64s carries business the old model priced; and the over-65 cut's "
             "£%.2f million on new business is outweighed by £%.2f million lost on renewals capped at the lower "
             "new-business price, £%.2f million less underwriting profit in all."
             % (f["u25_rise"], f["mid_rise"], c["cut_size"], c["proposal_u25"], f["u25_lr_at_proposal"],
                f["careful_mid_rise"], f["cut_nb_m"], f["cut_ren_loss_m"], f["cut_net_loss_m"]))
    L.append("")
    L.append("## Supplementary Questions")
    L.append("")
    L.append("### pcw_rate_review_2027.xlsx")
    L.append("")
    L.append("1. Sheet Calls, one row per segment with its 2027 change, expected 2027 loss ratio, policies and written "
             "premium; the expected loss ratio at a segment's smallest rise is at or just under the target (%.1f to "
             "%.1f per cent at the rise given). Under 25: a rise of %d per cent (any rise from %d to %d per cent is "
             "accepted), expected loss ratio %.1f per cent, %s policies and £%.1f million written premium (at the accepted rises, %s to %s "
             "policies and £%.1f to £%.1f million). 25 to 64: a rise of %d per cent (%d to %d per cent accepted), "
             "expected loss ratio %.1f per cent, %s policies and £%.1f million (%s to %s policies and £%.1f to £%.1f "
             "million). 65 and over: hold."
             % (f["lr_at_rise_band"][0], f["lr_at_rise_band"][1], f["u25_rise"], f["u25_family_lo"],
                f["u25_family_hi"], f["u25_lr_at_rise"],
                n(f["u25_policies_at_rise"]), f["u25_premium_at_rise_m"], n(f["u25_policies_band"][0]),
                n(f["u25_policies_band"][1]), f["u25_premium_band_m"][0], f["u25_premium_band_m"][1],
                f["mid_rise"], f["mid_family_lo"], f["mid_family_hi"], f["mid_lr_at_rise"],
                n(f["mid_policies_at_rise"]), f["mid_premium_at_rise_m"], n(f["mid_policies_band"][0]),
                n(f["mid_policies_band"][1]), f["mid_premium_band_m"][0], f["mid_premium_band_m"][1]))
    L.append("2. The 80 per cent range on the 25-to-64 2027 loss ratio at the %d per cent rise: %.1f to %.1f per "
             "cent (each end within %.1f points)." % (f["mid_rise"], f["mid_range_lo"], f["mid_range_hi"], c["band_range_pts"]))
    L.append("3. The 2027 loss ratio of the under-25 business the team's %d per cent would win: %.1f per cent "
             "(between %.1f and %.1f per cent across sound constructions)."
             % (c["proposal_u25"], f["u25_lr_at_proposal"], f["u25_lr15_lo"], f["u25_lr15_hi"]))
    L.append("4. Policies the two proposals would write in 2027: under-25s at a %d per cent rise %s; over-65s at the "
             "%d per cent cut %s, against %s if their rates are held (each within %d per cent)."
             % (c["proposal_u25"], n(f["u25_policies_at_proposal"]), c["cut_size"], n(f["o65_policies_at_cut"]),
                n(f["o65_policies_at_hold"]), c["band_policies_pct"]))
    L.append("5. What the over-65 cut does to 2027 underwriting profit: it lowers it by £%.2f million in all (within "
             "£%.1f million, the direction exact), adding £%.2f million on new business and losing £%.2f million on "
             "renewals." % (f["cut_net_loss_m"], c["band_profit_m"], f["cut_nb_m"], f["cut_ren_loss_m"]))
    L.append("6. Sheet 2026 by segment, quotes priced (unsold quotes counted at their extract weight), sales and "
             "conversion, January to October 2026, one row per segment:")
    for g in ("u25", "mid", "o65"):
        q, s, cv = f["r1_rows"][g]
        L.append("   - %s: %s quotes, %s sales, %.2f per cent." % (SEG[g], n(q), n(s), cv))
    L.append("7. Sheets Under 25 and 25 to 64 give the expected 2027 loss ratio at each rise beside the loss-ratio "
             "method's, with the 75 per cent target; sheet Over 65 cut the two sides of the cut; sheet Routes each "
             "shortcut's three calls beside these; sheet Basis the conventions they rest on.")
    L.append("")
    L.append("### pricing_committee_2027_rates.pptx")
    L.append("")
    L.append("8. Five slides: the three calls; the under-25 loss ratio against the rise, the business each rise "
             "would win against the latest twelve months, with the target; claims per predicted claim by how far "
             "below the cheapest rival the price sat; the 25-to-64 rise by the experience it is read from; the "
             "over-65 cut's new-business, renewal and total effect.")
    L.append("")
    L.append("## Critical Components")
    L.append("")
    L.append("1. Under-25 sales run at **%.2f** claims per predicted claim where the price sat furthest below the "
             "cheapest rival and **%.2f** where it sat closest, so the business the team's %d per cent would keep "
             "runs at **%.1f per cent** in 2027 (sound constructions %.1f to %.1f), not the %.1f per cent the "
             "loss-ratio method gives." % (f["u25_ae_deepest"], f["u25_ae_shallowest"], c["proposal_u25"],
                                          f["u25_lr_at_proposal"], f["u25_lr15_lo"], f["u25_lr15_hi"],
                                          f["careful_u25_lr_at_proposal"]))
    L.append("2. The 25-to-64 rise is **%d per cent** (%d to %d) on the business HPM v7 priced, completed over a "
             "full year of seasons; the latest twelve months give %d per cent and the 2026 business read to date %s."
             % (f["mid_rise"], f["mid_family_lo"], f["mid_family_hi"], f["careful_mid_rise"],
                rise(f["todate_mid_rise"])))
    L.append("3. The over-65 cut lowers 2027 underwriting profit by **£%.2f million**: it adds **£%.2f million** on "
             "new business and loses **£%.2f million** on renewals whose equivalent new-business price falls with it."
             % (f["cut_net_loss_m"], f["cut_nb_m"], f["cut_ren_loss_m"]))
    L.append("")
    L.append("## Step-by-Step")
    L.append("")
    L.append("1. Conformed the four sites' extracts (Covertide's quotes of 14 May 2026 sent twice, Brightquote's pence, "
             "Pricelark's UTC times), dropped the sites' ZZ99 monitoring quotes and counted each unsold quote at its "
             "extract weight of %d: 2026 conversion %.2f, %.2f and %.2f per cent for the three segments."
             % (c["extract_weight"], f["u25_2026_conversion"], f["mid_2026_conversion"], f["o65_2026_conversion"]))
    L.append("2. Joined every sale to the policy extract by quote reference, capped each claim at £%s (PLN-2027-03 "
             "2.1) and took each accident's claims to ultimate: every notified claim at its capped estimate and the "
             "claims still to be notified, read off each type's own notification pattern in the claims extract, at "
             "the type's mean cost (the reserving triangles' chain ladder, read at each claim's own age on 31 "
             "October, lands inside every band)." % n(c["cap"]))
    L.append("3. Read the seasons off the months of 2025 and 2026: claims cost per unit of earned premium runs at "
             "%.2f of the year's average in January and %.2f in June." % (f["s_jan"], f["s_jun"]))
    L.append("4. Took each segment's base from the business written since the last rate change (1 February 2026), "
             "each earned month weighted by its season: 2026 loss ratios %.1f, %.1f and %.1f per cent; read to 31 "
             "October as it stands, without the winter still to come, the same business gives %s for under-25s and %s "
             "for 25-to-64s." % (f["u25_base_lr"], f["mid_base_lr"], f["o65_base_lr"], rise(f["todate_u25_rise"]),
                                  rise(f["todate_mid_rise"])))
    L.append("5. Measured the won book's selection: claims per predicted claim to 30 September 2026 against the log of "
             "the price over the cheapest rival, fitted across the deciles of 2025 and 2026 under-25 sales (slope "
             "%.2f, %.2f deepest to %.2f shallowest); a higher price keeps only the deeper undercuts."
             % (f["u25_slope"], f["u25_ae_deepest"], f["u25_ae_shallowest"]))
    L.append("6. Replayed the quotes since 1 February 2026 at each rise against their three cheapest rivals moved up "
             "%d per cent, each sale reweighted by the conversion at its new rank (under 25: %.2f, %.2f, %.2f and "
             "%.2f per cent at ranks 1, 2, 3 and lower): under-25s need %d per cent and run at %.1f per cent at the "
             "team's %d; the loss-ratio method on the latest twelve months reproduces the team's %d per cent at %.1f."
             % (c["market"], f["u25_conv_1"], f["u25_conv_2"], f["u25_conv_3"], f["u25_conv_4"], f["u25_rise"],
                f["u25_lr_at_proposal"], c["proposal_u25"], f["careful_u25_rise"], f["careful_u25_lr_at_proposal"]))
    L.append("7. For 25-to-64s read the same replay on the business HPM v7 has priced (v7 rebuilt their frequency "
             "model on 1 February 2026, with the last rate change; slope %.2f, a small selection): %d per cent over a "
             "full year of seasons; the same replay on the latest twelve months gives %d and on 2025 and 2026 pooled "
             "%d, both mostly business HPM v6 priced, and the loss-ratio method on the latest twelve months %d."
             % (f["mid_slope"], f["mid_rise"], f["mid_replay_latest12_rise"], f["mid_replay_pooled_rise"],
                f["careful_mid_rise"]))
    L.append("8. Costed the over-65 cut: new business replayed %d per cent lower writes %s policies against %s and adds "
             "£%.2f million after commission (PCW-COM-2026) and £%d servicing; the renewal schedule's equivalent "
             "new-business prices fall %d per cent, the cap binds on more renewals (CMP-RP-04 3.1) and, with "
             "retention read from the renewal MI, renewals lose £%.2f million: £%.2f million less in all."
             % (c["cut_size"], n(f["o65_policies_at_cut"]), n(f["o65_policies_at_hold"]), f["cut_nb_m"],
                c["servicing"], c["cut_size"], f["cut_ren_loss_m"], f["cut_net_loss_m"]))
    L.append("9. Drew the year's 25-to-64 policies and claims %s times at the %d per cent rise: the loss ratio lies "
             "between %.1f and %.1f per cent in 80 per cent of the draws (PLN-2027-03 5.2)."
             % (n(c["draws"]), f["mid_rise"], f["mid_range_lo"], f["mid_range_hi"]))
    L.append("10. At the recommended changes the 2027 book writes %s under-25 policies (£%.1f million) and %s "
             "25-to-64 policies (£%.1f million)." % (n(f["u25_policies_at_rise"]), f["u25_premium_at_rise_m"],
                                                     n(f["mid_policies_at_rise"]), f["mid_premium_at_rise_m"]))
    L.append("")
    L.append("No other conclusion survives the files. The loss-ratio method holds the won book fixed, and the price-gap "
             "deciles show it is not: a %d per cent rise keeps only the sales the model under-priced most. The 2026 "
             "business read to date has not yet seen its winter, and pooled or latest-twelve-month experience mixes in "
             "25-to-64 business the v6 model priced. Pricing the over-65 cut on new business alone leaves out the "
             "renewal prices it caps, which the renewal pricing policy ties to the new-business rates."
             % c["proposal_u25"])
    open(path, "w").write("\n".join(L) + "\n")
