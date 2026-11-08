"""task9: submission.md, the four answer blocks, drafted from figures.json so every number is the generator's."""


def p(v, dp=1):
    v = 0.0 if round(v, dp) == 0 else v
    return ("%." + str(dp) + "f") % v


def text(F):
    G, D, E, L, ev, ll = F["golden"], F["default_path"], F["estimates"], F["lgd"], F["evidence"], F["loglik"]
    kl, os_ = G["KL"], G["OS"]
    rg = F["rungs"]
    hp, yl, hc, hh = rg["house_pooled_lgd"], rg["house_year_link"], rg["house_link_given_year"], rg["house_link_only"]
    hx = rg["house_link_closed"]
    LK, Ly, Lc = F["link"], F["link_year_only"], F["link_closed"]
    rb = F["recovery_by_other_defaults"]
    ci, cl, cb, cbl = rg["count_in_portfolio"], rg["count_in_portfolio_line"], rg["count_whole_book"], rg["count_whole_book_line"]
    gr, CK = F["grain"], F["count_link"]
    sub = p(F["subordination_pct"]["KL"], 1)
    subo = p(F["subordination_pct"]["OS"], 1)
    yk = ", ".join(p(v) for v in kl["by_year_pct"][:-1]) + " and " + p(kl["by_year_pct"][-1])
    yo = ", ".join(p(v) for v in os_["by_year_pct"][:-1]) + " and " + p(os_["by_year_pct"][-1])
    nk = "%d and %d" % tuple(kl["need_pct"])
    no = "%d and %d" % tuple(os_["need_pct"])
    word = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Quantitative Finance and Trading, Quantitative Finance (derivative pricing: the loss "
               "distribution of a senior note on a static portfolio of loans).  ")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## Final Recommendation\n")
    out.append(("**Buy neither note: Kestrel Lane's chance of any loss of principal over 2027 to 2031 is %s per cent "
                "and Ostvale's %s per cent, both above MP-RN-2's 1 per cent test, once each default recovers as the "
                "record shows defaults in its sponsor house's bad year recover.** This rejects Kestrel Lane's note, "
                "which passes at %s per cent only if every default loses one average share, and Ostvale's, which passes "
                "at %s per cent only if each default's recovery is read off the other defaults among the note's own "
                "loans, when Ostvale holds %s of each house's companies and recovery follows the house's whole year.\n")
               % (p(kl["p5_pct"]), p(os_["p5_pct"]), p(hp["KL"]["p5_pct"]), p(ci["OS"]["p5_pct"]),
                  word.get(int(gr["OS"]["loans_per_house_median"]), "%d" % gr["OS"]["loans_per_house_median"])))
    out.append("## Supplementary Questions\n")
    out.append("### ic_note_senior_notes_2027.docx\n")
    out.append("1. The recommendation: buy neither note; both fail MP-RN-2's 1 per cent test and the allocation stays in "
               "the cash and government bond sleeve (MP-RN-2 2.2).")
    out.append("2. Each note's chance of any loss of principal over 2027 to 2031: Kestrel Lane %s per cent; Ostvale %s "
               "per cent." % (p(kl["p5_pct"]), p(os_["p5_pct"])))
    out.append("3. Each portfolio's expected credit loss over 2027 to 2031, as a share of its par: Kestrel Lane %s per "
               "cent; Ostvale %s per cent." % (p(kl["el_pct"]), p(os_["el_pct"])))
    out.append("4. The subordination each note would need for chances of 1 and 0.5 per cent, in whole per cent of par "
               "rounded up: Kestrel Lane %s per cent (it offers %s); Ostvale %s per cent (it offers %s)."
               % (nk, sub, no, subo))
    out.append(("5. The chart: one log-scale panel, the five-year credit loss as a share of par from 0 to 30 per cent "
                "across, the chance it is exceeded up the side, one line per portfolio with Kestrel Lane's above "
                "Ostvale's in the tail, a vertical line at each note's subordination (Kestrel Lane %s, Ostvale %s per "
                "cent) where its line reads %s and %s per cent, and a horizontal line at the 1 per cent test.\n")
               % (sub, subo, p(kl["p5_pct"]), p(os_["p5_pct"])))
    out.append("### senior_note_loss_by_year.csv\n")
    out.append(("6. Ten rows, one per note and year end, columns note, issuer, subordination_pct, year_end and "
                "chance_of_loss_pct: Kestrel Lane %s per cent at the ends of 2027 to 2031; Ostvale %s per cent.\n")
               % (yk, yo))
    out.append("## Critical Components\n")
    out.append(("1. Companies held by one sponsor house default in the same years: pairs in the same house, sector and "
                "year defaulted together **%s per cent** of the time against **%s per cent** under different houses; "
                "the house's year carries **%s** of the variance the economy (**%s**) and the sector (**%s**) leave.")
               % (p(ev["same_house_same_sector_year_pct"], 2), p(ev["other_house_same_sector_year_pct"], 2),
                  p(E["ch"], 3), p(E["am"], 3), p(E["ak"], 3)))
    out.append(("2. On the 2008 to 2019 defaults, whose workouts have all closed, a default with no other default in "
                "its sponsor house in the calendar year of its default recovered **%s per cent** and one with three or "
                "more others **%s per cent**; "
                "the economy's year does not lower recovery (**%s** per unit of the year's shock).")
               % (p(rb["0"]["recovery_pct"]), p(rb["3"]["recovery_pct"]), p(Ly["bm"], 3)))
    out.append(("3. Those counts run over each house's whole book (a median of **%d** of the house's companies at risk "
                "in a defaulting house-year), while Ostvale's tape holds **%d** companies of each house and Kestrel "
                "Lane's **%d**; so recovery is tied to the house-year's own shock, inferred from that house-year's "
                "defaults against the rates its companies' ratings, ages and sector-years expected: **%s** plus **%s** "
                "per unit of the shock on the closed cohorts (and **%s** per unit of the year's).")
               % (CK["book_seen_median"], gr["OS"]["loans_per_house_median"], gr["KL"]["loans_per_house_median"],
                  p(LK["a"], 3), p(LK["bh"], 3), p(LK["bm"], 3)))
    out.append(("4. Kestrel Lane's **%d** loans sit with **%d** houses and Ostvale's **%d** with **%d**; the five-year "
                "chance of loss is **%s per cent** for Kestrel Lane's note at %s per cent subordination and **%s per "
                "cent** for Ostvale's at %s, both over the test (the sound estimators span %s to %s and %s to %s per "
                "cent).\n")
               % (kl["n"], kl["houses"], os_["n"], os_["houses"], p(kl["p5_pct"]), sub, p(os_["p5_pct"]), subo,
                  p(F["band_pct"]["KL"][0]), p(F["band_pct"]["KL"][1]), p(F["band_pct"]["OS"][0]),
                  p(F["band_pct"]["OS"][1])))
    out.append("## Step-by-Step\n")
    out.append(("1. Conformed lenderbase_loan_performance_2008-2026.csv (latest submission of each loan-quarter, the 2019 "
                "change of codes, older loans joined by name through lei_reference_extract_2026-12-31.csv): %s "
                "company-years at risk from 2008 to 2026 with %d defaults; traced every loan through "
                "dealtrail_buyout_transactions_1997-2026.csv to the buyout that began its ownership and the buyer's "
                "sponsor house (%d houses).") % ("{:,}".format(F["panel"]["company_years"]), F["panel"]["defaults"],
                                                F["panel"]["houses"]))
    out.append("2. Fitted one-year default chances by rating and full years since the buyout with a probit on the "
               "company-years.")
    out.append(("3. The usual copula, one factor fitted to the yearly default rates (%s) plus a sector factor (%s), "
                "gives Kestrel Lane %s per cent against Ostvale's %s per cent and would buy Kestrel Lane.")
               % (p(E["am"], 3), p(E["ak"], 3), p(D["KL"]["p5_pct"]), p(D["OS"]["p5_pct"])))
    out.append(("4. Pairs in the same house and year default together far more often than across houses, so the house's "
                "year enters the copula (%s of the residual variance, log-likelihood %s against %s for fund-years); with "
                "one average loss of %s per cent for every default (the 2008 to 2019 workouts, all closed) Kestrel Lane "
                "is at %s per cent and Ostvale at %s per cent: the reasonable but insufficient analysis, which buys "
                "Kestrel Lane.") % (p(E["ch"], 3), "{:,.1f}".format(ll["ll_h"]), "{:,.1f}".format(ll["ll_f"]),
                               p(L["lgd_pct"]), p(hp["KL"]["p5_pct"]), p(hp["OS"]["p5_pct"])))
    out.append(("5. Read the recoveries in lenderbase_workout_recoveries_2008-2026.csv against the economy's year: "
                "%s per unit of the year's shock, no lower in bad years, so a downturn link leaves Kestrel Lane at %s per "
                "cent and passing.")
               % (p(Ly["bm"], 3), p(yl["KL"]["p5_pct"])))
    out.append(("6. Read them against the house's year instead: on the closed 2008 to 2019 cohorts a lone default "
                "recovered %s per cent and one with three or more others in its house that year %s per cent; the "
                "clustered defaults also take longer, so %d workouts are still open and the later cohorts' closed "
                "cases are the quick, good ones, which is why the link is estimated on the 2008 to 2019 cohorts.")
               % (p(rb["0"]["recovery_pct"]), p(rb["3"]["recovery_pct"]), L["open"]))
    out.append(("7. Carrying that table to the notes by counting each default's co-defaults among the note's own loans "
                "puts Kestrel Lane at %s per cent and Ostvale at %s per cent and buys Ostvale (a straight line in the "
                "count gives %s and %s): the second reasonable but insufficient analysis. A default in the record shares "
                "its house-year with a median of %d of the house's companies, and Ostvale holds %d of each house's, so "
                "its defaults read as lone ones whatever year their house is having; the same default cannot recover "
                "more because the note holds fewer of its house's loans.")
               % (p(ci["KL"]["p5_pct"]), p(ci["OS"]["p5_pct"]), p(cl["KL"]["p5_pct"]), p(cl["OS"]["p5_pct"]),
                  CK["book_seen_median"], gr["OS"]["loans_per_house_median"]))
    out.append(("8. Inferred each house-year's shock as its posterior mean given the house-year's defaults against its "
                "companies' sector-year rates, and each year's from its default rate, and regressed recovery on both: "
                "%s plus %s per unit of the house-year's shock and %s per unit of the year's.")
               % (p(LK["a"], 3), p(LK["bh"], 3), p(LK["bm"], 3)))
    out.append(("9. Read both tapes into euros at the ECB rate of 31 December 2026 and simulated %s five-year paths "
                "under MP-RN-2, each default recovering on the year and house shocks that drew it: Kestrel Lane %s per "
                "cent at %s per cent subordination and Ostvale %s per cent at %s, expected credit losses of %s and %s "
                "per cent of par, and the year-end chances and the subordination needed above.\n")
               % ("{:,}".format(F["paths"]), p(kl["p5_pct"]), sub, p(os_["p5_pct"]), subo, p(kl["el_pct"]), p(os_["el_pct"])))
    bk, bo = F["band_pct"]["KL"], F["band_pct"]["OS"]
    out.append(("No other conclusion survives. Without the house's year in the dependence, with it but one average "
                "loss, or with a loss tied to the economy alone, the defaults that cluster in a house's bad year are "
                "priced at an ordinary recovery and Kestrel Lane is bought (at %s, %s or %s per cent); reading recovery "
                "off the co-defaults among each note's own loans prices Ostvale's defaults as lone ones and buys "
                "Ostvale (%s or %s per cent). Every estimate that ties recovery to the house's year keeps both notes "
                "over the test: the same co-default counts taken over each house's whole book in the record (%s and %s "
                "per cent, %s and %s with a straight line), the house-year's shock read against the year's rates (%s "
                "and %s), the house's shock alone (%s and %s), a cohort table or pair counts for the default model and "
                "the dependence with each house-year's shock read three ways (%s to %s and %s to %s per cent), and a link "
                "fitted on every closed workout, which drops "
                "the open ones MP-RN-2 4.1 keeps (%s and %s).\n")
               % (p(D["KL"]["p5_pct"]), p(hp["KL"]["p5_pct"]), p(yl["KL"]["p5_pct"]), p(ci["OS"]["p5_pct"]),
                  p(cl["OS"]["p5_pct"]), p(cb["KL"]["p5_pct"]), p(cb["OS"]["p5_pct"]), p(cbl["KL"]["p5_pct"]),
                  p(cbl["OS"]["p5_pct"]), p(hc["KL"]["p5_pct"]), p(hc["OS"]["p5_pct"]), p(hh["KL"]["p5_pct"]),
                  p(hh["OS"]["p5_pct"]), p(bk[0]), p(bk[1]), p(bo[0]), p(bo[1]), p(hx["KL"]["p5_pct"]),
                  p(hx["OS"]["p5_pct"])))
    return "\n".join(out)
