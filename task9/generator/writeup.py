"""task9: submission.md, the four answer blocks, drafted from figures.json so every number is the generator's."""

WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def p(v, dp=1):
    v = 0.0 if round(v, dp) == 0 else v
    return ("%." + str(dp) + "f") % v


def word(n):
    return WORD.get(int(n), "%d" % n)


def names(lst):
    lst = [x[0].lower() + x[1:] for x in lst]
    return ", ".join(lst[:-1]) + " and " + lst[-1] if len(lst) > 1 else lst[0]


def text(F):
    G, D, E, L, ev = F["golden"], F["default_path"], F["estimates"], F["lgd"], F["evidence"]
    kl, os_ = G["KL"], G["OS"]
    rg = F["rungs"]
    S, SE = F["sectors"], F["sector_evidence"]
    LK, Ly = F["link"], F["link_year_only"]
    rb = F["recovery_by_other_defaults"]
    gr, CK = F["grain"], F["count_link"]
    sk, so = p(F["subordination_pct"]["KL"]), p(F["subordination_pct"]["OS"])
    yk = ", ".join(p(v) for v in kl["by_year_pct"][:-1]) + " and " + p(kl["by_year_pct"][-1])
    yo = ", ".join(p(v) for v in os_["by_year_pct"][:-1]) + " and " + p(os_["by_year_pct"][-1])
    AB = F["ask_bands"]
    rng = lambda b, dp=1: "%s to %s" % (p(b[0], dp), p(b[1], dp)) if b[0] != b[1] else p(b[0], dp)
    irng = lambda b: "%d to %d" % (b[0], b[1]) if b[0] != b[1] else "%d" % b[0]
    ybk = ", ".join(rng(b) for b in AB["KL"]["by_year"][:-1]) + " and " + rng(AB["KL"]["by_year"][-1])
    ybo = ", ".join(rng(b) for b in AB["OS"]["by_year"][:-1]) + " and " + rng(AB["OS"]["by_year"][-1])
    hp, sol, hlp = rg["house_pooled_lgd"], rg["sector_one_lgd"], rg["house_link_pooled"]
    si, sio, yl = rg["sector_independent"], rg["sector_independent_one_lgd"], rg["house_year_link"]
    ci, cis, cb = rg["count_in_portfolio"], rg["count_in_portfolio_sector"], rg["count_whole_book"]
    bk, bo = F["band_pct"]["KL"], F["band_pct"]["OS"]
    swing = S["swing"]
    w = [y for y in SE["worst_years"]]
    lo = S["loadings"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Quantitative Finance and Trading, Quantitative Finance (derivative pricing: the loss "
               "distribution of a senior note on a static portfolio of loans).  ")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")

    out.append("## Final Recommendation\n")
    out.append(("**Buy neither note: Kestrel Lane's chance of any loss of principal over 2027 to 2031 is %s per cent at "
                "its %s per cent subordination and Ostvale's %s per cent at %s, both above MP-RN-2's 1 per cent test.** "
                "This rejects Kestrel Lane's note, which passes (%s per cent) only while every default loses one average "
                "share, when the defaults that cluster in its seven sponsor houses' bad years recover least, and "
                "Ostvale's, which passes (%s per cent) only while its five sectors are given the record's average swing "
                "with the economy, when their companies default together in the economy's bad years.\n")
               % (p(kl["p5_pct"]), sk, p(os_["p5_pct"]), so, p(sol["KL"]["p5_pct"]), p(hlp["OS"]["p5_pct"])))

    out.append("## Supplementary Questions\n")
    out.append("### ic_note_senior_notes_2027.docx\n")
    out.append("1. The recommendation: buy neither note; both fail MP-RN-2's 1 per cent test and the allocation stays in "
               "the cash and government bond sleeve (MP-RN-2 2.2).")
    out.append(("2. Each note's chance of any loss of principal over 2027 to 2031: Kestrel Lane %s per cent; Ostvale %s "
                "per cent. The sound estimators of the record's dependence (below) put them at %s and %s per cent.")
               % (p(kl["p5_pct"]), p(os_["p5_pct"]), rng(AB["KL"]["p5"]), rng(AB["OS"]["p5"])))
    out.append(("3. Each portfolio's expected credit loss over 2027 to 2031, as a share of its par: Kestrel Lane %s per "
                "cent; Ostvale %s per cent (the sound estimators %s and %s).")
               % (p(kl["el_pct"]), p(os_["el_pct"]), rng(AB["KL"]["el"]), rng(AB["OS"]["el"])))
    out.append(("4. The subordination each note would need for chances of 1 and 0.5 per cent, in whole per cent of par "
                "rounded up: Kestrel Lane %d and %d per cent (it offers %s; the sound estimators %s and %s); Ostvale %d "
                "and %d per cent (it offers %s; the sound estimators %s and %s).")
               % (kl["need_pct"][0], kl["need_pct"][1], sk, irng(AB["KL"]["need"][0]), irng(AB["KL"]["need"][1]),
                  os_["need_pct"][0], os_["need_pct"][1], so, irng(AB["OS"]["need"][0]), irng(AB["OS"]["need"][1])))
    out.append(("5. Table 3, the chance that each note has taken a loss by the end of each year, two rows (Kestrel Lane, "
                "Ostvale) and one column per year end from 2027 to 2031: Kestrel Lane %s per cent (the sound estimators "
                "%s); Ostvale %s per cent (%s).") % (yk, ybk, yo, ybo))
    out.append(("6. The chart: one log-scale panel, the five-year credit loss as a share of par from 0 to 30 per cent "
                "across, the chance it is exceeded up the side, one line per portfolio, a vertical line at each note's "
                "subordination (Kestrel Lane %s, Ostvale %s per cent) where its line reads %s and %s per cent, and a "
                "horizontal line at the 1 per cent test.\n") % (sk, so, p(kl["p5_pct"]), p(os_["p5_pct"])))

    out.append("## Critical Components\n")
    out.append(("1. Companies held by one sponsor house default in the same years: pairs in the same house, sector and "
                "year defaulted together **%s per cent** of the time against **%s per cent** under different houses, "
                "and the house's year carries **%s** of each company's credit standing.")
               % (p(ev["same_house_same_sector_year_pct"], 2), p(ev["other_house_same_sector_year_pct"], 2),
                  p(F["house_share"], 3)))
    out.append(("2. The economy's year weighs on five sectors far more than on the rest: %s load **%s to %s** on it "
                "against **%s** at most for the other eleven (one loading for all, %s, fits the record %s log-likelihood "
                "points worse); their default rates rise together (%s per cent in %d against %s for the rest), so "
                "Ostvale's portfolio, wholly in those sectors, loads **%s** against Kestrel Lane's **%s**.")
               % (names(swing), p(S["swing_min"], 2), p(S["swing_max"], 2), p(S["rest_max"], 2), p(S["pooled_l"], 3),
                  p(S["ll_gain"]), p(SE["swing_rate_pct"][str(w[0])]), w[0],
                  p(SE["rest_rate_pct"][str(w[0])]), p(os_["loading"], 2), p(kl["loading"], 2)))
    out.append(("3. Recovery follows the sponsor house's year, not the economy's: on the 2008 to 2019 defaults, whose "
                "workouts have all closed, a default with no other default in its house that calendar year recovered "
                "**%s per cent** and one with three or more others **%s per cent**, while the economy's year alone "
                "moves recovery **%s** per unit; on each house-year's shock, inferred from its defaults across the "
                "house's whole book, recovery runs **%s** plus **%s** per unit.")
               % (p(rb["0"]["recovery_pct"]), p(rb["3"]["recovery_pct"]), p(Ly["bm"], 3), p(LK["a"], 3),
                  p(LK["bh"], 3)))
    out.append(("4. With both carried into the simulation, Kestrel Lane's chance of loss is **%s per cent** at %s per "
                "cent subordination and Ostvale's **%s per cent** at %s; the sound estimators span %s to %s and %s to %s "
                "per cent, every one over the test.\n")
               % (p(kl["p5_pct"]), sk, p(os_["p5_pct"]), so, p(bk[0]), p(bk[1]), p(bo[0]), p(bo[1])))

    out.append("## Step-by-Step\n")
    out.append(("1. Conformed lenderbase_loan_performance_2008-2026.csv (latest submission of each loan-quarter, the 2019 "
                "change of codes, older loans joined by name through lei_reference_extract_2026-12-31.csv): %s "
                "company-years at risk from 2008 to 2026 with %d defaults; traced every loan through "
                "dealtrail_buyout_transactions_1997-2026.csv to the buyout that began its ownership and the buyer's "
                "sponsor house (%d houses). Fitted one-year default chances by rating and full years since the buyout.")
               % ("{:,}".format(F["panel"]["company_years"]), F["panel"]["defaults"], F["panel"]["houses"]))
    out.append(("2. The agencies' copula, the economy's year and one sector factor, with every default losing the "
                "average of the default years whose workouts have all closed (%s per cent, MP-RN-2 4.1), puts Kestrel "
                "Lane at %s per cent and Ostvale at %s: the quick answer, %s.")
               % (p(L["lgd_pct"]), p(D["KL"]["p5_pct2"], 2), p(D["OS"]["p5_pct2"], 2), D["call"]))
    out.append(("3. Pairs in the same house and year default together far more often than across houses, so the house's "
                "year enters the copula (%s of each standing); with one average loss of %s per cent (the 2008 to 2019 "
                "workouts) Kestrel Lane is at %s per cent and Ostvale at %s, and the fund would buy %s.")
               % (p(F["house_share"], 3), p(L["lgd_pct"]), p(hp["KL"]["p5_pct2"], 2), p(hp["OS"]["p5_pct2"], 2),
                  hp["call"]))
    out.append(("4. Read the sixteen sectors' yearly default rates against the year: %s rise and fall together (their "
                "yearly rates correlate %s with each other, the other sectors' %s), so each sector gets its own "
                "loading on the shared year (%s to %s against at most %s). Given larger factors of their own instead, "
                "one sector at a time, Ostvale's defaults would not arrive together and the house route still files "
                "%s (Kestrel Lane %s, Ostvale %s); with the loadings and one average loss, Ostvale fails at %s per cent "
                "and Kestrel Lane passes at %s: the second insufficient answer, Kestrel Lane.")
               % (names(swing), p(SE["swing_corr_within"], 2), p(SE["rest_corr_within"], 2), p(S["swing_min"], 2),
                  p(S["swing_max"], 2), p(S["rest_max"], 2), sio["call"], p(sio["KL"]["p5_pct2"], 2),
                  p(sio["OS"]["p5_pct2"], 2), p(sol["OS"]["p5_pct2"], 2), p(sol["KL"]["p5_pct2"], 2)))
    out.append(("5. Read the recoveries in lenderbase_workout_recoveries_2008-2026.csv against the economy's year: %s "
                "per unit, no lower in bad years (a bad economy brings defaults from houses having ordinary years), so "
                "a downturn link leaves Kestrel Lane at %s per cent. Against the house's year: a lone default recovered "
                "%s per cent and one with three or more others %s; the defaults in a house's bad years also take "
                "longer (%s years in the worst third of house-years on the closed cohorts against %s in the best), so the "
                "%d workouts still open sit in worse house-years than the recent closed ones, and MP-RN-2 4.1 reads "
                "recovery from the default years whose workouts have all closed, 2008 to 2019.")
               % (p(Ly["bm"], 3), p(yl["KL"]["p5_pct2"], 2), p(rb["0"]["recovery_pct"]), p(rb["3"]["recovery_pct"]),
                  p(F["open_evidence"]["worst_third_years"]), p(F["open_evidence"]["best_third_years"]), L["open"]))
    out.append(("6. Counting each default's co-defaults among the note's own loans prices Ostvale's defaults as lone "
                "ones (Kestrel Lane %s per cent, Ostvale %s) and buys Ostvale: a default in the record shares its "
                "house-year with a median of %d of the house's companies, and Ostvale holds %s of each house's. So each "
                "house-year's shock is inferred as its posterior mean given that house-year's defaults across the "
                "house's whole book, against its companies' sector-year rates, and recovery regressed on it: %s plus %s "
                "per unit (and %s per unit of the year's shock).")
               % (p(ci["KL"]["p5_pct2"], 2), p(ci["OS"]["p5_pct2"], 2), CK["book_seen_median"],
                  word(gr["OS"]["loans_per_house_median"]), p(LK["a"], 3), p(LK["bh"], 3), p(LK["bm"], 3)))
    out.append(("7. Tied to the house's year but with one pooled loading on the economy, recovery takes Kestrel Lane "
                "to %s per cent while Ostvale stays at %s and is bought: the third insufficient answer. Ostvale's "
                "economy-driven defaults come from houses having ordinary years and recover well, so only the sectors' "
                "joint swing takes its tail past the test.")
               % (p(hlp["KL"]["p5_pct2"], 2), p(hlp["OS"]["p5_pct2"], 2)))
    out.append(("8. Read both tapes into euros at the ECB rate of 31 December 2026 and simulated %s five-year paths "
                "under MP-RN-2, each sector's loading on the year, the house's year, and each default recovering on the "
                "shocks that drew it: Kestrel Lane %s per cent at %s per cent subordination and Ostvale %s per cent at "
                "%s, expected credit losses of %s and %s per cent of par, and the year-end chances and the "
                "subordination needed above.\n")
               % ("{:,}".format(F["paths"]), p(kl["p5_pct"]), sk, p(os_["p5_pct"]), so, p(kl["el_pct"]),
                  p(os_["el_pct"])))
    out.append(("No other conclusion survives. One average recovery passes Kestrel Lane on every route that keeps it "
                "(the copula %s, the house's year %s, the sector loadings %s, the economy's year %s per cent), and Ostvale "
                "passes on one pooled loading (%s), on larger sector factors of their own (%s) or on its own thin slices "
                "of each house (%s). Every estimate that carries both strands keeps both notes over the test: %d variants from %s to %s "
                "per cent for Kestrel Lane and %s to %s for Ostvale, and the record's co-default counts over each "
                "house's whole book (%s and %s).\n")
               % (p(D["KL"]["p5_pct2"], 2), p(hp["KL"]["p5_pct2"], 2), p(sol["KL"]["p5_pct2"], 2), p(yl["KL"]["p5_pct2"], 2),
                  p(hlp["OS"]["p5_pct2"], 2), p(si["OS"]["p5_pct2"], 2), p(cis["OS"]["p5_pct2"], 2),
                  len(F["band_members"]), p(bk[0]), p(bk[1]), p(bo[0]), p(bo[1]), p(cb["KL"]["p5_pct2"], 2),
                  p(cb["OS"]["p5_pct2"], 2)))
    return "\n".join(out)
