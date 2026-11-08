"""task9: submission.md, the four answer blocks, drafted from figures.json so every number is the generator's."""


def p(v, dp=2):
    return ("%." + str(dp) + "f") % v


def text(F):
    G, D, E, L, ev, ll = F["golden"], F["default_path"], F["estimates"], F["lgd"], F["evidence"], F["loglik"]
    kl, os_ = G["KL"], G["OS"]
    rg = F["rungs"]
    sub = p(F["subordination_pct"]["KL"], 1)
    yk = ", ".join(p(v) for v in kl["by_year_pct"][:-1]) + " and " + p(kl["by_year_pct"][-1])
    yo = ", ".join(p(v) for v in os_["by_year_pct"][:-1]) + " and " + p(os_["by_year_pct"][-1])
    nk = "%s, %s and %s" % tuple(p(v, 1) for v in kl["need_pct"])
    no = "%s, %s and %s" % tuple(p(v, 1) for v in os_["need_pct"])
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Quantitative Finance and Trading, Quantitative Finance (derivative pricing: the loss "
               "distribution of a senior note on a static portfolio of loans).  ")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## Final Recommendation\n")
    out.append(("**Buy Ostvale's Class A note: its chance of any loss of principal over 2027 to 2031 is %s per cent, "
                "inside MP-RN-2's 1 per cent test, while Kestrel Lane's is %s per cent and fails it.** The usual copula "
                "that links defaults only through the economy and the sector gives Kestrel Lane %s per cent against "
                "Ostvale's %s per cent and would buy Kestrel Lane, but it leaves out the years in which a sponsor "
                "house's companies fail together, which Kestrel Lane's concentration in %s houses turns into the "
                "fatter tail.\n") % (p(os_["p5_pct"]), p(kl["p5_pct"]), p(D["KL"]["p5_pct"]), p(D["OS"]["p5_pct"]),
                                     {5: "five", 6: "six", 4: "four", 7: "seven"}.get(kl["houses"], str(kl["houses"]))))
    out.append("## Supplementary Questions\n")
    out.append("### ic_note_senior_notes_2027.docx\n")
    out.append("1. The recommendation: buy Ostvale's Class A note; Kestrel Lane's note fails MP-RN-2's 1 per cent test "
               "and is not bought.")
    out.append("2. Each note's chance of any loss of principal over 2027 to 2031: Kestrel Lane %s per cent; Ostvale %s "
               "per cent." % (p(kl["p5_pct"]), p(os_["p5_pct"])))
    out.append("3. The subordination each note would need for chances of 1, 0.5 and 0.25 per cent: Kestrel Lane %s per "
               "cent of par (it offers %s); Ostvale %s per cent of par (it offers %s)." % (nk, sub, no, sub))
    out.append(("4. The chart: one log-scale panel, the five-year credit loss as a share of par from 0 to 30 per cent "
                "across, the chance it is exceeded up the side, one line per portfolio with Kestrel Lane's above "
                "Ostvale's in the tail, a vertical line at both notes' %s per cent subordination where the lines "
                "read %s and %s per cent, and a horizontal line at the 1 per cent test.\n")
               % (sub, p(kl["p5_pct"]), p(os_["p5_pct"])))
    out.append("### senior_note_loss_by_year.csv\n")
    out.append(("5. Ten rows, one per note and year end, columns note, issuer, subordination_pct, year_end and "
                "chance_of_loss_pct: Kestrel Lane %s per cent at the ends of 2027 to 2031; Ostvale %s per cent.\n")
               % (yk, yo))
    out.append("## Critical Components\n")
    out.append(("1. Companies held by one sponsor house default in the same years: pairs in the same house, sector and "
                "year defaulted together **%s per cent** of the time against **%s per cent** for pairs in the same "
                "sector and year under other houses, while pairs in the same house but different years sit at the "
                "independence rate (**%s** against **%s per cent**).")
               % (p(ev["same_house_same_sector_year_pct"]), p(ev["other_house_same_sector_year_pct"]),
                  p(ev["same_house_other_year_pct"], 3), p(ev["independent_pair_pct"], 3)))
    out.append(("2. The house's year carries **%s** of the variance of a borrower's credit standing that the economy "
                "(**%s**) and the sector (**%s**) leave, and it fits the record better than a fund-year or a lasting "
                "house or fund effect.") % (p(E["ch"], 3), p(E["am"], 3), p(E["ak"], 3)))
    out.append("3. Kestrel Lane's **%d** loans sit with **%d** houses; Ostvale's **%d** loans with **%d**."
               % (kl["n"], kl["houses"], os_["n"], os_["houses"]))
    out.append("4. Each default loses **%s per cent**, the average shortfall on the 2008 to 2019 defaults whose workouts "
               "have all closed." % p(L["lgd_pct"], 1))
    bk, bo = F["band_pct"]["KL"], F["band_pct"]["OS"]
    out.append(("5. At %s per cent subordination the five-year chance of loss is **%s per cent** for Kestrel Lane, which "
                "fails the test, and **%s per cent** for Ostvale, which passes; across sound estimates of the record "
                "(a probit or a cohort table for the default rates, a random effect or pair counts for the dependence) "
                "Kestrel Lane stays between %s and %s per cent and Ostvale between %s and %s per cent.\n")
               % (sub, p(kl["p5_pct"]), p(os_["p5_pct"]), p(bk[0], 1), p(bk[1], 1), p(bo[0], 1), p(bo[1], 1)))
    out.append("## Step-by-Step\n")
    out.append(("1. Conformed lenderbase_loan_performance_2008-2026.csv (latest submission of each loan-quarter, the 2019 "
                "change of codes, LEIs only from 2012 with older loans joined by name through "
                "lei_reference_extract_2026-12-31.csv): %s company-years at risk from 2008 to 2026 (each loan reported performing or on "
                "watch at the previous year end, or outstanding at the start of the record in 2008) with %d defaults.")
               % ("{:,}".format(F["panel"]["company_years"]), F["panel"]["defaults"]))
    out.append(("2. Traced every loan through dealtrail_buyout_transactions_1997-2026.csv to the completed buyout that "
                "began the ownership it sits in and to the buyer's sponsor house (the name its funds share): %d "
                "houses, no loan unlinked.") % F["panel"]["houses"])
    out.append("3. Fitted one-year default chances by rating and full years since that buyout with a probit on the "
               "company-years.")
    out.append(("4. The usual copula, one factor fitted to the yearly default rates (%s) plus a sector factor (%s), "
                "matches the record's yearly and sector-year default counts and gives Kestrel Lane %s per cent against "
                "Ostvale's %s per cent: the reasonable but insufficient analysis, which would buy Kestrel Lane.")
               % (p(E["am"], 3), p(E["ak"], 3), p(D["KL"]["p5_pct"]), p(D["OS"]["p5_pct"])))
    out.append(("5. Counted joint defaults among pairs at risk in the same year: %s per cent for the same house, sector "
                "and year against %s per cent across houses, and %s per cent for the same house in different years, "
                "the independence rate, so the dependence is a house's shared bad year, not a weak house.")
               % (p(ev["same_house_same_sector_year_pct"]), p(ev["other_house_same_sector_year_pct"]),
                  p(ev["same_house_other_year_pct"], 3)))
    out.append(("6. Estimated the house-year component as a random effect on house-year clusters given the sector-year: "
                "%s, with a log-likelihood of %s against %s for fund-years and %s for a lasting fund effect.")
               % (p(E["ch"], 3), "{:,.1f}".format(ll["ll_h"]), "{:,.1f}".format(ll["ll_f"]),
                  "{:,.1f}".format(ll["ll_q"])))
    out.append(("7. Took the loss on default from the %d closed workouts on 2008 to 2019 defaults, %s per cent; the "
                "average over every closed workout (%s per cent) leaves out the %d open workouts, which are the long "
                "ones that recover less.") % (L["n_mature"], p(L["lgd_pct"], 1), p(L["lgd_closed_pct"], 1), L["open"]))
    out.append(("8. Read both tapes into euros at the ECB rate of 31 December 2026, gave each borrower its house and "
                "years since buyout, and simulated %s five-year paths under MP-RN-2: Kestrel Lane %s per cent and "
                "Ostvale %s per cent at %s per cent subordination, with the year-end chances and subordination needs "
                "above.\n") % ("{:,}".format(F["paths"]), p(kl["p5_pct"]), p(os_["p5_pct"]), sub))
    out.append(("No other conclusion survives. Every model without the house's year buys Kestrel Lane and is "
                "contradicted by the same-year house pairs; reading the dependence at the fund, or as a lasting fund "
                "effect, also buys Ostvale but fits the record worse and leaves Kestrel Lane at %s or %s per cent; the "
                "closed-workout loss on default keeps the call (%s against %s per cent) but understates loss because "
                "the open workouts are the long ones; and MP-RN-2 4.2 rules out an assumed correlation or a "
                "fat-tailed copula.\n") % (p(rg["fund_year"]["KL"]["p5_pct"]), p(rg["fund_persistent"]["KL"]["p5_pct"]),
                                          p(rg["closed_lgd"]["KL"]["p5_pct"]), p(rg["closed_lgd"]["OS"]["p5_pct"])))
    return "\n".join(out)
