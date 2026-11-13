"""task24: submission.md, the four answer blocks, every figure from figures.json (one set of numbers everywhere)."""

TN = {"order_delivery": "orders and delivery", "returns_refunds": "returns and refunds",
      "account_billing": "account and billing", "product_howto": "product how-to",
      "device_troubleshooting": "device troubleshooting"}
TYPES = list(TN)
VOLS = (20000, 40000, 60000, 80000, 120000)


def k(n):
    return "{:,}".format(int(n))


def row(FG, key):
    """one scenario's figures: each ticket type and the 2027 mix"""
    t = FG[key]
    return "; ".join("%s %.1f" % (TN[x], t[x]) for x in TYPES) + "; 2027 mix %.1f" % t["mix"]


def buys(p):
    if not p["reach"]:
        return "finds no purchase within the vendors' limits that reaches the bar"
    parts = []
    if p["option"]:
        parts.append("%s comparisons of the option" % k(p["option"]))
    if p["desk"]:
        parts.append("%s Ardentdesk comparisons" % k(p["desk"]))
    return "buys " + " and ".join(parts) + " (USD %s)" % k(round(p["cost"]))


def submission(FG, BANDS, SC):
    """FG: figures.json; BANDS: the graded bands; SC: the shortcut figures the blocks name"""
    trb = "device_troubleshooting"
    rec = FG["R7_purchase"]
    b = BANDS
    lines = ["# task24 answer blocks", "", "## Final Recommendation", ""]
    lines.append(
        "Buy %s Ardentdesk device troubleshooting comparisons (USD %s) and take none of the Tallyfield option: with "
        "the signed order, the Q1 2027 reward model is then expected to reach %.1f per cent accuracy against the senior "
        "technicians on the planned 2027 mix (80 per cent range %.1f to %.1f), at the %.1f per cent bar. This rejects "
        "reading the dashboard's IS-25 agreement through the reviews by a constant, which %s, counting labels or "
        "weighting them by accuracy, which %s, and leaving out the crowd's pull to longer replies, which %s."
        % (k(rec["desk"]), k(FG["R7_cost_usd"]), FG["R7_at_purchase_mix"], FG["R8_range"]["lo"], FG["R8_range"]["hi"],
           FG["bar_pct"], buys(SC["J1"]), buys(SC["J2"]), buys(SC["J3"])))
    lines += ["", "## Supplementary Questions", ""]
    ve = FG["R1_vendor_error"]
    lines.append(
        "1. The spreadsheet gives each vendor's error against the standard by ticket type: the share of its 2026 audit "
        "judgments (no-preference judgments set aside) whose reply is not the one at least two of the three senior "
        "technicians chose, every audit pair counted, in per cent to one decimal. Tallyfield: %s. Ardentdesk: %s. "
        "Graded within %.1f points on each cell."
        % ("; ".join("%s %.1f" % (TN[t], ve["tallyfield.%s" % t]) for t in TYPES),
           "; ".join("%s %.1f" % (TN[t], ve["ardentdesk.%s" % t]) for t in TYPES), b["vendor"]))
    lines.append(
        "2. Each ticket type's expected accuracy against the standard, and the 2027 mix's (each type weighted by its "
        "share of the 2027 plan's tickets), in per cent to one decimal. The current model, RM-22: %s. Graded within "
        "%.1f points on each ticket type and %.1f on the mix." % (row(FG, "R2_current"), b["type"], b["mix"]))
    lines.append(
        "3. With the signed order alone (300,000 comparisons, no-preference judgments not used in training): %s."
        % row(FG, "R3_order"))
    for i, x in enumerate(VOLS):
        lines.append("%d. With %s Ardentdesk comparisons added: %s." % (4 + i, k(x), row(FG, "R4_%d" % x)))
    n = 4 + len(VOLS)
    lines.append(
        "%d. With the whole Tallyfield option taken up (300,000 more comparisons, no Ardentdesk): %s. Items 3 to %d "
        "are graded within %.1f points on each ticket type and %.1f on the mix." % (n, row(FG, "R5_option"), n,
                                                                                  b["type"], b["mix"]))
    tr = FG["tranches"]
    lines.append(
        "%d. The purchase: %s Ardentdesk comparisons and none of the option, USD %s at USD 3.60 a comparison, expected "
        "%.1f per cent on the 2027 mix. Each 10,000 of the option (USD %s) saves about 1,000 Ardentdesk comparisons, "
        "so a tranche or two beside the desk costs little more (10,000 of the option with %s Ardentdesk, USD %s more; "
        "30,000 with %s, USD %s more) while larger volumes do not pay; graded on Ardentdesk carrying the purchase, "
        "between %s and %s Ardentdesk comparisons with no more than 30,000 of the option, the cost following the volume."
        % (n + 1, k(rec["desk"]), k(FG["R7_cost_usd"]), FG["R7_at_purchase_mix"], k(FG["context"]["option_tranche_cost_usd"]),
           k(tr["10000"]["desk"]),
           k(tr["10000"]["extra_usd"]), k(tr["30000"]["desk"]), k(tr["30000"]["extra_usd"]), k(b["desk"][0]),
           k(b["desk"][1])))
    lines.append(
        "%d. The 80 per cent range of the 2027-mix accuracy at that purchase: %.1f to %.1f per cent, from a bootstrap of "
        "every record the estimate rests on (the audit's pairs, IS-25's pairs with every run's pick, each review "
        "round's drafts, the deliveries); graded on a range that holds the expected accuracy, each end within %.1f "
        "points. The same bootstrap puts the Ardentdesk volume the bar needs between %s and %s."
        % (n + 2, FG["R8_range"]["lo"], FG["R8_range"]["hi"], b["range"], k(FG["vol_range"]["lo"]), k(FG["vol_range"]["hi"])))
    lines.append(
        "%d. The one-page memo states the recommendation: buy %s Ardentdesk comparisons, take none of the Tallyfield "
        "option, expected %.1f per cent against the %.1f per cent bar." % (n + 3, k(rec["desk"]), FG["R7_at_purchase_mix"],
                                                                           FG["bar_pct"]))
    lines += ["", "## Critical Components", ""]
    lines.append(
        "1. The current model is at %.1f per cent on the 2027 mix against the standard (%.1f on device "
        "troubleshooting), not the %.1f per cent the dashboard shows: IS-25's labels are single 2025 Tallyfield "
        "judgments, so a run's agreement with them is set by its accuracy, the labels' own error (guideline v2, fitted "
        "on the seven reviewed runs) and the pull to longer replies the run shares with the crowd. Read through the "
        "reviews by a constant per ticket type the current model comes out at %.1f; read at the 2026 audit's crowd "
        "error, which the reviewed runs reject, at %.1f." % (FG["R2_current"]["mix"], FG["R2_current"][trb],
                                                           FG["R2_dashboard_RM22"], SC["J1_current_mix"],
                                                           SC["is_audit_current"]))
    lines.append(
        "2. A Tallyfield judgment on a device troubleshooting pair carries about %.2f of an Ardentdesk judgment's "
        "information: the audit puts the crowd's error there at %.0f per cent when it is not pulled to the longer "
        "reply and the desk's at %.0f, and what a label teaches the model goes with the square of its signal. So the "
        "signed order's %s troubleshooting comparisons lift the mix only to %.1f per cent, and the whole option adds "
        "%.1f points for USD 126,000, where %s Ardentdesk comparisons add %.1f for USD %s. Weighted by accuracy "
        "(%.2f) or counted, the option looks like the cheaper way to the bar."
        % (FG["info_ratio_troubleshooting"], FG["derived"]["crowd_error_troubleshooting_pct"],
           FG["derived"]["desk_error_troubleshooting_pct"], k(FG["order_troubleshooting"]), FG["R3_order"]["mix"],
           FG["derived"]["option_gain_pts"], k(rec["desk"]),
           FG["derived"]["purchase_gain_pts"], k(FG["R7_cost_usd"]), FG["acc_ratio_troubleshooting"]))
    lines.append(
        "3. The crowd's pull to the longer reply grows with the length gap, and a model takes on %.2f of its labels' "
        "pull in proportion to their crowd share: it costs accuracy against the technicians while it raises agreement "
        "with IS-25. Left out, the 2026 runs read as learning less from their labels than they did, and the cheapest "
        "way to the bar %s." % (FG["kappa"], buys(SC["J3"]).replace("buys", "looks like buying")))
    lines.append(
        "4. The purchase is %s Ardentdesk comparisons and none of the option, expected %.1f per cent (80 per cent range "
        "%.1f to %.1f) at the %.1f per cent bar, USD %s." % (k(rec["desk"]), FG["R7_at_purchase_mix"], FG["R8_range"]["lo"],
                                                            FG["R8_range"]["hi"], FG["bar_pct"], k(FG["R7_cost_usd"])))
    lines += ["", "## Step-by-Step", ""]
    lines.append(
        "1. Assemble the records: drop the three Tallyfield batches exported twice after the June platform move (by "
        "comparison id), set aside no-preference judgments (paid, never used in training), map Ardentdesk's left and "
        "right choices through the reply shown on the left, keep one row per run and pair where an evaluation job was "
        "re-run from its checkpoint, and read the review form's 'first' and 'second' (rounds 1 to 3) as replies A and "
        "B. The register's usable counts by vendor and ticket type then match the deliveries.")
    lines.append(
        "2. Read each vendor's error against the standard from the audit (item 1); Tallyfield's own gold-question "
        "accuracy (an error of %.1f per cent on every ticket type) measures its gold bank, not the technicians. Then "
        "fit one latent-class model by ticket type over the audit and the reviews' technician votes: the share of "
        "pairs with no better reply, each technician's error, each vendor's error and the crowd's pull to the longer "
        "reply, the pull's shape by length ratio from every usable 2026 Tallyfield judgment. Each label's information "
        "is the square of its signal, the gap between its chance of naming a reply when it is the better one and when "
        "it is not: about %.2f of a desk label for a crowd label on device troubleshooting."
        % (SC["quick_vendor_error"], FG["info_ratio_troubleshooting"]))
    lines.append(
        "3. Fit every run at once: each run's accuracy on pairs with a better reply on one learning curve in label "
        "information by ticket type (a shared bend), its pull a share of its labels' crowd share, measured against "
        "the technicians in the seven shadow reviews and through IS-25, whose agreement with a run depends on the "
        "run's accuracy, IS-25's own label error (guideline v2, fitted on the reviewed runs; the audit's v3 error is "
        "rejected by a likelihood ratio of %.0f) and the pull the run shares with the crowd. The hurried pass reads "
        "IS-25 plus a constant per type from the reviewed runs; IS-25 is almost blind on device troubleshooting, so "
        "every purchase looks short of the bar." % FG["is_error_lr"])
    lines.append(
        "4. Forecast the Q1 2027 model (every usable 2026 comparison plus Q1 2027's) by ticket type and on the plan's "
        "mix for the signed order, the whole option and each Ardentdesk volume; each type stops short of 100 per cent "
        "because the technicians split on the pairs with no better reply, which no run learns. A separate bend for "
        "each type does not improve the fit (likelihood ratio %.1f on %d degrees of freedom). A curve rising with log "
        "labels and no bound puts device troubleshooting at %.1f with 120,000 Ardentdesk comparisons, against %.1f."
        % (FG["alpha_lr"], FG["alpha_df"], SC["J4_trb120"], SC["golden_trb120"]))
    lines.append(
        "5. Search every purchase within the vendors' terms (the option in steps of 10,000 up to 300,000; Ardentdesk "
        "at least 10,000 in steps of 1,000 up to 120,000) for the cheapest that reaches %.1f per cent: %s Ardentdesk "
        "comparisons and no option, USD %s. Bootstrap the records for the 80 per cent range, %.1f to %.1f."
        % (FG["bar_pct"], k(rec["desk"]), k(FG["R7_cost_usd"]), FG["R8_range"]["lo"], FG["R8_range"]["hi"]))
    lines.append(
        "6. Why no other conclusion survives: eight defensible variants (a logistic curve in log information, the "
        "pull on the square root of the crowd share, plain error rates, coarser length bins, no-preference judgments "
        "counted, the audit alone for the technicians, the pull read from the audit, the reviews alone) all buy "
        "Ardentdesk only, between %s and %s comparisons, and each fitted input moved by its bootstrap spread keeps a "
        "purchase Ardentdesk carries. The shortcuts each make a different call: the constant bridge %s; accuracy weights "
        "%s; counting %s; no pull %s." % (k(SC["family_lo"]), k(SC["family_hi"]), buys(SC["J1"]), buys(SC["J2"]),
                                          buys(SC["J2raw"]), buys(SC["J3"])))
    return "\n".join(lines) + "\n"
