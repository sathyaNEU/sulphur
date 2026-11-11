"""task9: submission.md, the four answer blocks, written from figures.json (F) and the pack's own names. Every figure
here is read from F; the words around them are the author's."""
import pack as PK
import params as P

DECK, BOOK = "Harbourne_2027_plan_review.pptx", "Harbourne_2027_plan_workbook.xlsx"


def um(v):
    """USD millions as the committee states them, to the nearest million."""
    return "USD %s million" % "{:,.0f}".format(v)


def n0(v):
    return "{:,.0f}".format(v)


def band(b):
    return "between %s and %s" % (n0(b[0]), n0(b[1]))


def pband(b, k=2):
    f = "%." + str(k) + "f"
    return "between %s%% and %s%%" % (f % b[0], f % b[1])


def joined(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(F, path):
    pl, rt, inc = F["platform"], F["routes"], {x["pod"]: x for x in F["increases"]}
    fail, either = F["R6_fail"], F["R6_either"]
    added = F["R6_added"]
    G = list(F["R1_alpha"])
    cr = "Credit"
    pp = F["past_plans"]
    over = [y for y, v in pp.items() if v["expected"] > v["earned"]]
    gap = F["past_gap"]
    rec = F["record"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Quantitative Finance and Trading, Quantitative Finance (strategy backtesting and evaluation: a multi-manager "
             "platform's capital plan across its portfolio-manager pods).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## Final Recommendation\n")
    L.append("**Plan %s of net P&L for 2027 at the draft capital plan** (sound methods land %s, USD million), four years in five between %s and %s, "
             "and **approve the draft without the increases for %s**, %s pods whose %s of added capital is expected to earn %.1f%% to %.1f%% a "
             "year after payout and funding against the 1.5%% hurdle (%s sit%s close enough to the hurdle that sound methods split on %s). "
             "It rejects the %s the draft shows when each pod's three-year return on capital is carried to its new capital, as past plans "
             "were priced, and the %s that comes from reading alpha on the risk model's factors and drawing the year a day at a time, "
             "with each increase judged on the pod's return at its new size, a reading that passes %s." % (
                 um(F["R4_net"]), band(F["R4_band"]), um(F["R5_range"]["P10"]), um(F["R5_range"]["P90"]), joined(fail),
                 "four credit" if len(fail) == 4 else "the", um(added), min(inc[p]["per_dollar"] for p in fail), max(inc[p]["per_dollar"] for p in fail),
                 joined(either), "s" if len(either) == 1 else "", "it" if len(either) == 1 else "them",
                 um(F["quick"]["mean"]), um(rt["careful but hurried"]["mean"]),
                 joined([p for p in fail if p not in rt["careful but hurried"]["fail"]])))
    L.append("")
    L.append("## Supplementary Questions\n")
    L.append("### %s\n" % BOOK)
    L.append("1. A first sheet that leads with the expected 2027 net P&L after PM payouts at the draft plan, **%s** (%s), built from the "
             "pods' expected trading P&L of %s less funding of %s (the bill rate of %.2f%% on the review date plus 0.35%% on 20%% of capital), "
             "PM payouts of %s paid pod by pod and the 2027 budget's platform costs of %s; and its 80%% range, **%s to %s** (the 10th "
             "percentile %s, the 90th %s), the year's markets drawn from the record a quarter at a time with every pod under the drawdown "
             "rules." % (um(F["R4_net"]), band(F["R4_band"]), um(pl["trade"]), um(pl["funding"]), pl["bill"], um(pl["payouts"]), um(pl["costs"]),
                         um(F["R5_range"]["P10"]), um(F["R5_range"]["P90"]), band(F["R5_bands"]["P10"]), band(F["R5_bands"]["P90"])))
    L.append("2. The pods whose increases fall short of the 1.5%% hurdle: **%s**, each with its 2026 and 2027 capital, the capital it adds "
             "and the net P&L each dollar of it is expected to add a year (%s). %s are borderline: their margin over the hurdle is inside "
             "what sound methods differ by, so either call stands. The other %d increases clear it. Without the four, the plan expects %s "
             "(%s): the increases add little P&L, and the point is the %s of capital they would tie up below the hurdle." % (
                 joined(fail), "; ".join("%s %.2f%%" % (p, inc[p]["per_dollar"]) for p in fail), joined(either),
                 len(F["R6_pass"]), um(F["R7_net"]), band(F["R7_band"]), um(added)))
    L.append("3. For each strategy group, its alpha a year since January 2017, as a per cent of capital, net of what a passive holding "
             "of its markets earned with their carry: %s." % "; ".join("%s %.2f%% (%s)" % (g, F["R1_alpha"][g], pband(F["R1_bands"][g])) for g in G))
    L.append("4. A pod's alpha per dollar falls by **%.1f%%** when its capital doubles (%s), read within pods; across pods the record "
             "shows %.1f%%." % (F["R3_fall"], pband(F["R3_band"], 1), F["R3_rivals"]["pooled"]))
    L.append("5. The workbook also carries every increase, every pod's expected edge and 2027 P&L, the groups' alpha beside the risk "
             "model's specific P&L, and a sensitivity sheet that changes one judgment at a time.")
    L.append("\n### %s\n" % DECK)
    L.append("6. About six slides for the committee: the plan and the four increases to drop on the first; a bridge from the pods' "
             "trading P&L to net P&L; each increase's net P&L per dollar added against the hurdle, the failing ones marked; alpha by "
             "strategy group with the risk model's figure beside it; capacity within pods against across them; and what the plan "
             "rests on, with the figure each shorter route gives.")
    L.append("\n## Critical Components\n")
    L.append("1. The expected 2027 net P&L at the draft plan is **%s** (%s), with an 80%% range of **%s to %s** (the 10th percentile "
             "%s, the 90th %s)." % (um(F["R4_net"]), band(F["R4_band"]), um(F["R5_range"]["P10"]), um(F["R5_range"]["P90"]),
                                    band(F["R5_bands"]["P10"]), band(F["R5_bands"]["P90"])))
    L.append("2. The increases below the 1.5%% hurdle are **%s** (%s borderline either way); every other increase clears it." % (
        joined(fail), joined(either)))
    L.append("3. A pod's alpha per dollar falls by **%.1f%%** for each doubling of its capital (%s), read within pods; across pods "
             "the record shows only %.1f%%, because capital has followed records." % (F["R3_fall"], pband(F["R3_band"], 1), F["R3_rivals"]["pooled"]))
    L.append("4. Credit's alpha a year since January 2017 is **%.2f%%** of capital (%s), net of the Baa spread a passive holding "
             "earns; on the risk model's factors it reads %.2f%%." % (F["R1_alpha"][cr], pband(F["R1_bands"][cr]), F["R1_risk_model"][cr]))
    L.append("\n## Step-by-Step\n")
    L.append("1. `%s` and `%s` are the risk system's daily P&L before and after the 3 July 2023 migration; the second states P&L "
             "in USD thousands and capital in USD millions. `%s` maps the pod codes re-issued on 1 April 2022, the legacy file carries "
             "12 March 2021 twice (%d duplicate rows) and has no rows on %s, whose P&L sits in the next day's row. On one footing the "
             "record is %s pods over %s days, and each pod's month agrees with `%s` once the month-end true-ups are moved back a day." % (
                 PK.F["legacy"], PK.F["current"], PK.F["codes"], rec["dupes"], joined(rec["missing"]), n0(rec["pods"]), n0(rec["days"]),
                 PK.F["admin"]))
    L.append("2. Alpha (policy section 7) is P&L beyond a passive holding of the markets a pod trades, on the series the platform keeps. "
             "A holding earns its price move and its carry: the 10-year's yield over the bill, the Baa spread over the 10-year, a G10 "
             "basket's interest differential (long the three highest 3-month rates, short the three lowest, each leg earning its own "
             "rate). Each pod's daily return on capital is regressed on those holdings; a group's alpha is its pods' alpha P&L over "
             "their capital-years. Credit comes to %.2f%%. The hurried analysis uses `%s`, whose factors carry only price moves: credit's "
             "specific P&L is %.2f%%, the spread it earned left in. Monthly regressions, a lag of each factor, a two- or four-a-side carry "
             "basket and the group's own markets alone all land inside every band." % (F["R1_alpha"][cr], PK.F["riskmodel"], F["R1_risk_model"][cr]))
    L.append("3. Capacity (policy 8e) is fitted as alpha per dollar falling by the same share at any size, alpha = a(K/150m)^-b, on "
             "pod-years with 120 or more trading days and a separate a for each pod: b = %.3f, %.1f%% per doubling. Across pods (one a "
             "for all) b = %.3f, %.1f%%: the committee gives more capital to stronger records (policy section 2), so across pods size "
             "and skill rise together. Weighting pod-years by days, pod-quarters and the onboarding steps alone give %.1f%% to %.1f%%." % (
                 F["theta"]["pod"], F["R3_fall"], F["theta"]["pooled"], F["R3_rivals"]["pooled"],
                 min(F["R3_rivals"][k] for k in ("pod-weighted", "pod-quarter", "ramp")), max(F["R3_rivals"][k] for k in ("pod-weighted", "pod-quarter", "ramp"))))
    L.append("4. Each pod's edge at USD 150 million is read from its own residual, each day weighted by its capital's capacity factor, "
             "and pulled toward its group's by how much the group's pods really differ beyond their records' noise (a normal prior "
             "per group). The draft raises the pods with the best three-year records, and part of a short record is luck: taken at face "
             "value the year shows %s." % um(rt["each pod's own record"]["mean"]))
    L.append("5. The year (policy 8a to 8d): %s simulated years, the markets drawn from the record a quarter at a time with their "
             "means set to zero, each pod at its 2027 capital (onboarding pods on their schedule) with its loadings and its own noise, "
             "halved or closed by the drawdown rules, funded at %.2f%% plus 0.35%% on a fifth of its capital, paid 18%% of its own "
             "positive year, less platform costs of %s: %s, the 10th percentile %s and the 90th %s. Capacity read on pod-quarters, "
             "pod-years weighted by days or the onboarding steps, priors fitted by maximum likelihood or with one spread for all "
             "groups, and markets drawn a month or half a year at a time all land inside the bands. Drawing the markets a day at a "
             "time loses credit's weeks-long runs and puts the 10th percentile at %s; on the risk model's factors the year is %s; "
             "taking each pod's record at face value gives %s and leaving the drawdown rules out %s. The careful but hurried "
             "analysis, on the risk model's factors with days drawn one at a time, gets %s, %s to %s, and with the carry netted alone "
             "still %s to %s." % (
                 n0(pl["sims"]), pl["bill"], um(pl["costs"]), um(F["R4_net"]), um(F["R5_range"]["P10"]), um(F["R5_range"]["P90"]),
                 um(rt["daily resampling"]["p10"]), um(rt["risk model's factors"]["mean"]), um(rt["each pod's own record"]["mean"]),
                 um(rt["no drawdown rules"]["mean"]), um(rt["careful but hurried"]["mean"]), um(rt["careful but hurried"]["p10"]),
                 um(rt["careful but hurried"]["p90"]), um(rt["careful but hurried, carry netted"]["p10"]), um(rt["careful but hurried, carry netted"]["p90"])))
    L.append("6. The hurdle (policy section 9): each increase is run at its 2026 and its 2027 capital on the same simulated years, and "
             "the difference in its expected net P&L after payout and funding is divided by the capital it adds. %s come to %s. Judged "
             "instead on the pod's net return on its whole new capital, which is not what the added dollar earns once alpha per dollar "
             "falls with size, %s fail%s. On the risk model's factors %s clear%s the hurdle, and with each record at face value %s "
             "do%s; read across pods, only %s fails." % (
                 joined(fail), joined(["%.2f%%" % inc[p]["per_dollar"] for p in fail]),
                 joined(rt["average return at the new size"]["fail"]) or "none", "s" if len(rt["average return at the new size"]["fail"]) == 1 else "",
                 joined([p for p in fail if p not in rt["risk model's factors"]["fail"]]) or "none",
                 "s" if len([p for p in fail if p not in rt["risk model's factors"]["fail"]]) == 1 else "",
                 joined([p for p in fail if p not in rt["each pod's own record"]["fail"]]) or "none",
                 "es" if len([p for p in fail if p not in rt["each pod's own record"]["fail"]]) == 1 else "",
                 joined(rt["capacity across pods"]["fail"]) or "none"))
    L.append("7. `%s` shows what the house pricing has done before: each plan since 2018 expected more of its pods than they went on "
             "to earn in %d of the %d completed years, by %s a year on average (`%s`, net of payouts, less each year's platform "
             "costs)." % (PK.F["plans"], len(over), len(pp), um(gap), PK.F["admin"]))
    L.append("")
    L.append("No other plan survives the files. The policy plans alpha with the markets at zero, so a pod's return on capital, which "
             "carries the market and carry returns it rode, is not what a pod is expected to earn, and the past plans priced that way "
             "ran ahead of their pods in %d years of %d. Credit's spread is what a passive holding earns, so it cannot be a credit "
             "pod's alpha; capital has always followed records, so only the pods' own histories show what size costs; a record of a "
             "few years is part luck, and the draft rewards the luckiest; and the drawdown rules and pod-by-pod payouts are part of "
             "the year the policy plans. Every sound way of reading each of those lands the plan %s and the same four increases below "
             "the hurdle." % (len(over), len(pp), band(F["R4_band"])))
    open(path, "w").write("\n".join(L) + "\n")
