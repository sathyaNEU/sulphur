"""figures.json and submission.md, both written from the golden's own objects (every figure in the four answer blocks
is printed from here, at its stated precision, with its band where reasonable methods differ)."""
import json

import golden as GD
import params as P

CH_SHORT = {"SOC": "paid social", "SEA": "paid search", "PART": "cashback partners", "TEL": "telemarketing",
            "APP": "app-store campaigns", "DIR": "direct"}


def pct(x):
    return "%.1f" % (100 * x)


def figures(G):
    g, b = G["golden"], G["bands"]
    F = {"hurdle": P.HURDLE, "horizon_months": P.HORIZON, "budget": g["budget"], "plan_total": int(sum(G["spend"].values())),
         "lines_in_plan": len(G["plan"]), "funded": [GD.key(l) for l in g["R8"]], "n_funded": len(g["R8"]),
         "careful_funded": [GD.key(l) for l in G["routes"]["careful"]["R8"]],
         "careful_budget": int(sum(G["spend"][l] for l in G["routes"]["careful"]["R8"])),
         }
    F["paying_oct"] = {t: int(v) for t, v in g["R1"].items()}
    F["paying_oct_total"] = int(sum(g["R1"].values()))
    F["value_2023q3"] = {c: int(round(v)) for c, v in g["R2"].items()}
    F["stepup_share"] = {o: round(100 * v, 1) for o, v in g["R3"].items()}
    F["stepup_added"] = {o: round(100 * v, 1) for o, v in g["R4"].items()}
    F["survival_36"] = {c: round(100 * v, 1) for c, v in g["R5"].items()}
    F["rise_extra"] = {t: int(round(v)) for t, v in g["R6"].items()}
    F["rise_extra_total"] = int(round(sum(g["R6"].values())))
    F["plan_paying"] = {c: int(round(v)) for c, v in g["R9"].items()}
    F["plan_paying_total"] = int(sum(F["plan_paying"].values()))
    F["plan_starts"] = G["n_plan_starts"]
    F["plan_starts_total"] = int(sum(G["n_plan_starts"].values()))
    F["line_value"] = {GD.key(l): int(round(v)) for l, v in g["R7"].items()}
    F["line_cost"] = {GD.key(l): round(G["cps"][l], 2) for l in G["plan"]}
    F["line_multiple"] = {GD.key(l): round(g["R7"][l] / G["cps"][l], 2) for l in G["plan"]}
    F["line_spend"] = {GD.key(l): int(G["spend"][l]) for l in G["plan"]}
    bands = {}
    for r, scale, nd in [("R2", 1, 0), ("R3", 100, 1), ("R4", 100, 1), ("R5", 100, 1), ("R6", 1, 0), ("R7", 1, 0),
                         ("R9", 1, 0)]:
        bands[r] = {GD.key(k): [round(lo * scale, nd), round(hi * scale, nd)] for k, (lo, hi) in b[r].items()}
    F["bands"] = bands
    F["careful"] = {"line_value": {GD.key(l): int(round(v)) for l, v in G["routes"]["careful"]["R7"].items()},
                    "survival_36": {c: round(100 * v, 1) for c, v in G["routes"]["careful"]["R5"].items()},
                    "rise_extra_total": int(round(sum(G["routes"]["careful"]["R6"].values()))),
                    "value_2023q3": {c: int(round(v)) for c, v in G["routes"]["careful"]["R2"].items()},
                    "plan_paying_total": int(round(sum(G["routes"]["careful"]["R9"].values())))}
    F["routes_funded"] = {nm: [GD.key(l) for l in r["R8"]] for nm, r in G["routes"].items()}
    F["rivals_funded"] = {nm: [GD.key(l) for l in r["R8"]] for nm, r in G["rivals"].items()}
    if "boot" in G:
        B = G["boot"]
        F["resampled"] = {"draws": B["reps"], "same_lines": B["same"],
                          "low": {GD.key(l): round(v, 2) for l, v in B["lo"].items()},
                          "high": {GD.key(l): round(v, 2) for l, v in B["hi"].items()}}
    own = G["newest_own"]
    F["newest_own"] = {"cancellations_min": min(o for o, e in own.values()),
                       "cancellations_max": max(o for o, e in own.values()),
                       "cancellations": int(sum(o for o, e in own.values())),
                       "expected": int(round(sum(e for o, e in own.values())))}
    unf = [l for l in G["plan"] if l not in g["R8"]]
    F["best_left_out"] = round(max(g["R7"][l] / G["cps"][l] for l in unf), 2)
    F["margin_min_pct"] = int(100 * min(abs(g["R7"][l] / G["cps"][l] / P.HURDLE - 1) for l in G["plan"]))
    return F


def band_txt(F, r, k, unit=""):
    lo, hi = F["bands"][r][k]
    if r in ("R3", "R4", "R5"):
        return "%.1f to %.1f%s" % (lo, hi, unit)
    return "%s to %s%s" % (f"{int(lo):,}", f"{int(hi):,}", unit)


def submission(F, path):
    order = sorted(F["line_value"], key=lambda k: -F["line_multiple"][k])
    funded = [k for k in order if k in F["funded"]]
    extra = [k for k in F["careful_funded"] if k not in F["funded"]]
    unf = [k for k in order if k not in F["funded"]]

    L = ["# task1: Medienhaus Brückenhafen, 2027 digital acquisition lines\n", "## Tags\n",
         "**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer "
         "lifetime value).", "**Analytical objective:** Forecasting & Predictive Modeling.\n"]
    L.append("## Final Recommendation\n")
    L.append("Fund %d of the plan's %d lines (%s) for a budget of EUR %s: each is expected to bring at least %.1f "
             "times its planned cost per start over 36 months (%.2f to %.2f), while the best line left out runs %.2f. "
             "Not the %d lines for EUR %s that a reading of each line's newest starts on its older starts' "
             "survival, of the end of the introductory price without the April 2027 list prices and of returns on "
             "the customer number puts over the bar, which adds %s." % (
                 F["n_funded"], F["lines_in_plan"], ", ".join(funded), f"{F['budget']:,}", F["hurdle"],
                 min(F["line_multiple"][k] for k in funded), max(F["line_multiple"][k] for k in funded),
                 F["best_left_out"], len(F["careful_funded"]), f"{F['careful_budget']:,}", ", ".join(extra)))
    L.append("\n## Supplementary Questions\n")
    L.append("### acquisition_lines_2027.xlsx\n")
    L.append("1. Sheet Lines 2027 has one row per line of the plan, %d rows ordered by multiple of cost, highest "
             "first, with columns line, channel, title, 2027 offer, planned starts, planned spend (EUR), planned "
             "cost per start (EUR), expected 36-month net revenue per start (EUR), multiple of cost and funded "
             "(yes or no), then the budget for the funded lines. The expected 36-month net revenue per start, in "
             "euros (band in brackets): " % F["lines_in_plan"] + "; ".join(
                 "%s %s (%s)" % (k, f"{F['line_value'][k]:,}", band_txt(F, "R7", k)) for k in order) + ".")
    L.append("2. The planned cost per start is the plan's spend on the line over its planned starts; the multiple of "
             "cost is the expected value over it, and the funded column reads yes on %s." % ", ".join(funded))
    L.append("\n### acquisition_note_2027.pdf\n")
    q = []
    q.append("One page. It opens with the lines to fund, %s, and the budget they need, EUR %s, with a table of the "
             "funded lines' cost per start, 36-month value and multiple." % (", ".join(funded), f"{F['budget']:,}"))
    q.append("Paying digital subscribers at 31 October 2026, by title (exact): " + "; ".join(
        "%s %s" % (P.TITLE_NAME[t], f"{F['paying_oct'][t]:,}") for t in P.TITLES) + "; %s in all." % (
        f"{F['paying_oct_total']:,}"))
    q.append("Of the plan's 2027 starts, with every line run as planned, the number still paying on 31 December "
             "2027, by channel: " + "; ".join(
                 "%s %s of %s (%s)" % (CH_SHORT[c], f"{F['plan_paying'][c]:,}", f"{F['plan_starts'][c]:,}",
                                       band_txt(F, "R9", c)) for c in P.PAID) + "; %s of %s in all." % (
                 f"{F['plan_paying_total']:,}", f"{F['plan_starts_total']:,}"))
    q.append("For each 2027 offer, the share of its starts leaving when the introductory price ends at 2026 list "
             "prices, in per cent: " + "; ".join(
                 "%s %.1f (%s)" % (o, F["stepup_share"][o], band_txt(F, "R3", o)) for o in F["stepup_share"]) + ".")
    q.append("The percentage points the April 2027 list prices add to that share: " + "; ".join(
        "%s %.1f (%s)" % (o, F["stepup_added"][o], band_txt(F, "R4", o)) for o in F["stepup_added"]) + ".")
    q.append("Extra cancellations the April 2027 rise brings by 31 December 2027 among the subscriptions paying at "
             "31 October 2026, by title: " + "; ".join(
                 "%s %s (%s)" % (P.TITLE_NAME[t], F["rise_extra"][t], band_txt(F, "R6", t)) for t in P.TITLES)
             + "; %s in all." % F["rise_extra_total"])
    q.append("Share of the November 2025 to April 2026 starts still paying three years after they started, in per "
             "cent, by channel: " + "; ".join(
                 "%s %.1f (%s)" % (CH_SHORT[c], F["survival_36"][c], band_txt(F, "R5", c)) for c in P.CHANNELS) + ".")
    q.append("Net revenue per start the July to September 2023 starts brought in over their first 36 months, with "
             "later subscriptions by the same household, in euros, by channel: " + "; ".join(
                 "%s %s (%s)" % (CH_SHORT[c], F["value_2023q3"][c], band_txt(F, "R2", c)) for c in P.CHANNELS) + ".")
    for i, x in enumerate(q, 3):
        L.append("%d. %s" % (i, x))
    L.append("\n## Critical Components\n")
    soc = sorted(k for k in F["line_value"] if k.startswith("SOC"))
    L.append("1. Every line's expected 36-month net revenue per start (forecasting): the funded lines run **%.2f to "
             "%.2f** times their cost; the paid social lines come to %s and the cashback lines at the Rundschau and "
             "the Kreisblatt to **EUR %s** and **EUR %s**, all under 3.5 times their cost." % (
                 min(F["line_multiple"][k] for k in funded), max(F["line_multiple"][k] for k in funded),
                 ", ".join("%s **EUR %s**" % (k, F["line_value"][k]) for k in soc), F["line_value"]["PART-BHR"],
                 F["line_value"]["PART-KBO"]))
    L.append("2. The newest starts' survival (missingness and measurement): **%.1f per cent** of the paid social "
             "starts of November 2025 to April 2026 and **%.1f per cent** of the cashback starts are still paying three "
             "years in (%.1f and %.1f on their channels' older starts' survival); paid search's **%.1f per cent** is "
             "above its older starts' %.1f." % (F["survival_36"]["SOC"], F["survival_36"]["PART"],
                                                F["careful"]["survival_36"]["SOC"], F["careful"]["survival_36"]["PART"],
                                                F["survival_36"]["SEA"], F["careful"]["survival_36"]["SEA"]))
    L.append("3. The full price at the end of the introduction (causal reasoning): the April 2027 list prices add "
             "**%.1f to %.1f points** to the share leaving when an introductory price ends." % (
                 min(F["stepup_added"].values()), max(F["stepup_added"].values())))
    L.append("4. Returns by household (data discovery): the July to September 2023 starts brought **EUR %s** per "
             "start on paid social and **EUR %s** direct over 36 months counted by household (EUR %s and EUR %s on "
             "the customer number alone)." % (F["value_2023q3"]["SOC"], F["value_2023q3"]["DIR"],
                                              F["careful"]["value_2023q3"]["SOC"], F["careful"]["value_2023q3"]["DIR"]))
    L.append("\n## Step-by-Step\n")
    for i, s_ in enumerate(STEPS(F), 1):
        L.append("%d. %s" % (i, s_))
    L.append("")
    close = ("No other conclusion survives the records. Completing the newest starts on their channel's older "
             "survival is ruled out by the reading log, where the starts of the twelve months to October 2026 read "
             "less (paid social, cashback) or more (paid search) and the leaving rate follows reading; calibrating "
             "each line on its own newest starts instead rests on %d to %d full-price cancellations a line so far "
             "(%d in all, against %d the reading-based model expects of them), too few to set a line's rate; an "
             "end-of-intro model without the full price is ruled out by the step-ups either side of April 2025; the "
             "customer number as the household is ruled out by the payment fingerprints and addresses that customer "
             "numbers share; and every reasonable variant of the reading measure, the tenure terms, the offer terms "
             "in either model and the household links funds the same %d lines, every line at least %d per cent "
             "from the bar." % (F["newest_own"]["cancellations_min"], F["newest_own"]["cancellations_max"],
                                F["newest_own"]["cancellations"], F["newest_own"]["expected"], F["n_funded"],
                                F["margin_min_pct"]))
    if "resampled" in F:
        close += (" Drawing whole start months again within each line and refitting every model, %d of %d draws "
                  "fund the same lines." % (F["resampled"]["same_lines"], F["resampled"]["draws"]))
    L.append(close)
    open(path, "w").write("\n".join(L) + "\n")


def STEPS(F):
    return [
        "From subscriptions_2023-01_2026-10.csv, price_periods_2023-01_2026-10.csv and customers.csv, drop the "
        "repeated export rows, the staff, gift and company products and the test accounts (the KPI standard), map the "
        "renamed channel codes, and count the subscriptions charged on 31 October 2026: %s in all (Rundschau %s), "
        "where every exported row charged in October gives more." % (f"{F['paying_oct_total']:,}",
                                                                      f"{F['paying_oct']['BHR']:,}"),
        "Link households across customer numbers through payment_methods.csv (the payment fingerprint) and "
        "customers.csv (the normalised address), as the KPI standard counts households: the July to September 2023 starts "
        "brought EUR %s per start on paid social over 36 months, not the EUR %s on the customer number alone." % (
            F["value_2023q3"]["SOC"], F["careful"]["value_2023q3"]["SOC"]),
        "Fit the end of the introductory price on every step-up in the record by offer, channel and title with a "
        "term for the full price the start steps up to (offer_catalogue.csv, price_list_digital_2027.pdf), which "
        "the step-ups either side of the April 2025 rise identify: at 2026 prices the 2027 offers lose %.1f per "
        "cent of their starts (the annual offer) to %.1f (the free quarter), and the April 2027 prices add %.1f to "
        "%.1f points, where a period term for the 2025 jump adds nothing." % (
            min(F["stepup_share"].values()), max(F["stepup_share"].values()), min(F["stepup_added"].values()),
            max(F["stepup_added"].values())),
        "Join reading_by_login_2024-01_2026-10.csv to logins.csv and sum each customer's logins; fit the "
        "full-price leaving rate on months since the step-up, channel and the first three months' reading, and "
        "complete the young starts on their own reading: %.1f per cent of the paid social starts of November 2025 "
        "to April 2026 are still paying three years in, not the %.1f their channel's older starts imply." % (
            F["survival_36"]["SOC"], F["careful"]["survival_36"]["SOC"]),
        "Read the April 2025 rise's extra cancellations from the cancellations received after the February 2025 "
        "notice letters through the second month at the new price, against each paid-tenure band's own rate, and "
        "carry them to each subscription's paid tenure at the April 2027 rise, which gives %s extra cancellations "
        "by 31 December 2027 (the KPI standard's extra cancellations), not the %s an after-the-date, pooled reading gives." % (
            F["rise_extra_total"], F["careful"]["rise_extra_total"]),
        "Carry the plan's %s planned starts month by month through their introductory prices, the end of intro at "
        "the April 2027 list prices and the full-price leaving rate on their own reading: %s still paying on 31 "
        "December 2027 (paid social %s of %s), where the shortcuts above leave %s." % (
            f"{F['plan_starts_total']:,}", f"{F['plan_paying_total']:,}", F["plan_paying"]["SOC"],
            F["plan_starts"]["SOC"], f"{F['careful']['plan_paying_total']:,}"),
        "Value each line of media_plan_2027.xlsx by survival arithmetic over its planned start months, the reading "
        "and payment routes of its starts in the twelve months to October 2026 (as the KPI standard takes them), its 2027 offer at "
        "the April 2027 prices, the store fees and the household's first return through the paywall inside "
        "the 36 months: from EUR %s per start (SEA-BHR) down to EUR %s (TEL-ELN)." % (
            F["line_value"]["SEA-BHR"], F["line_value"]["TEL-ELN"]),
        "Fund the lines at 3.5 times their planned cost per start or more (the KPI standard): %d lines for EUR %s; the "
        "shortcuts above together fund %d lines for EUR %s." % (F["n_funded"], f"{F['budget']:,}",
                                                               len(F["careful_funded"]), f"{F['careful_budget']:,}"),
    ]


def write(G, fig_path, sub_path):
    F = figures(G)
    json.dump(F, open(fig_path, "w"), indent=1, sort_keys=True, ensure_ascii=False)
    submission(F, sub_path)
    return F
