"""task20: submission.md, the four answer blocks, every figure from figures.json; each banded figure carries the range
the defensible variants span."""
import datetime as dt

MONTH = {"2025-07": "July", "2025-08": "August", "2025-09": "September", "2025-10": "October", "2025-11": "November",
         "2025-12": "December"}


def nice(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def dates(lst):
    return ", ".join(nice(x) for x in lst)


FN = {"pc": "pc_daily_pnl_SMCF_2024-07-01_2025-06-30.csv", "runlog": "ere_run_log_SMCF_2024-06-28_2025-06-30.csv",
      "backtest": "SMCF_VaR_backtest_2025Q2.xlsx", "method": "ERE_equity_VaR_methodology_note.pdf",
      "eqx1": "eqx_position_extract_v1_2024-06-28_2025-01-17.csv", "eqx2": "eqx_position_extract_v2_2025-01-17_2025-06-30.csv",
      "xwalk": "eqx_v2_instrument_crosswalk.csv", "futs": "futs_position_snapshots_2024-06-28_2025-06-30.csv",
      "vendor": "vendor_eod_closes_SMCF_universe_2022-05-31_2025-06-30.csv",
      "blotter": "oms_trade_blotter_SMCF_2024-07-01_2025-06-30.csv", "plan": "SMCF_H2_2025_business_plan.xlsx",
      "mapping": "ere_proxy_mapping_vintages_2024Q2_2025Q2.csv"}


def text(F):
    hc, hd, B = F["heading_counts"], F["heading_dates"], F["bands"]
    sc = F["shortcut_counts"]
    add = F["addon_m"]
    ab = B["addon"]
    mo = [MONTH[m] for m in F["addon_months"]]
    L = []
    a = L.append
    a("# task20 submission: why the SMCF desk breached its VaR, and the add-on for the second half")
    a("")
    a("## Tags")
    a("")
    a("**Domain:** Quantitative Finance and Trading, Quantitative Finance (risk modeling: one-day 99% VaR backtesting and "
      "exception attribution for an equity facilitation desk).")
    a("**Analytical objective:** Root-Cause Analysis.")
    a("")
    a("## Final Recommendation")
    a("")
    a("**Report %d exceptions for the 250 days to 30 June 2025 and count %d of them against the model: %d are the inputs', "
      "every one a night ERE's extract was cut before the closing-auction allocations were booked, %d is other income, and "
      "a sound model shows %d (the %s zone, %d to %d across the settings MRS-4 allows); hold an add-on of USD %.2f million "
      "in July that falls to nil by December.** This rejects the official %d booked exceptions and red zone, the reading "
      "that blames the %d runs on an older extract (they caused none, and it leaves %d against the model), and an add-on "
      "held at July's figure or rising with the plan's ramp to USD %.2f million."
      % (F["exceptions_total"], F["model_count"], hc["inputs"], hc["income"], F["sound_count"], F["sound_zone"].lower(),
         B["sound_count"][0], B["sound_count"][1], add[0], F["official_count"], F["outage_runs"],
         F["careful_model_count"], F["addon_ramp_only_m"][-1]))
    a("")
    a("## Supplementary Questions")
    a("")
    a("### exception_classification_2025Q2.xlsx")
    a("")
    a("1. Every exception dated under one MRS-4 heading, the headings adding back to %d, on an Exceptions sheet with one "
      "row per date (booked and hypothetical P&L, the VaR reported and its run, which P&L shows it, the heading, ERE's VaR "
      "on the book held, the own-history and volatility-scaled VaRs, the allocations missing from the run, and the "
      "basis): (a) other income %d: %s; (b) inputs %d: %s; (c) risks not in the model %d: %s; (d) volatility %d: %s; (e) "
      "model accuracy %d: %s. Across decay 0.94 to 0.97, scaled at the portfolio or name by name, %s move between (d) "
      "and (e) (volatility %d to %d, model accuracy %d to %d); every other row holds."
      % (F["exceptions_total"], hc["income"], dates(hd["income"]), hc["inputs"], dates(hd["inputs"]), hc["omitted"],
         dates(hd["omitted"]), hc["volatility"], dates(hd["volatility"]), hc["sound"], dates(hd["sound"]),
         " and ".join(nice(x) for x in F["flex_dates"]), B["volatility"][0], B["volatility"][1], B["accuracy"][0],
         B["accuracy"][1]))
    a("2. What went wrong with ERE's inputs, on an Engine inputs sheet with one row per run (extract read, whether it "
      "was an older one, the allocations booked after its cut, the VaR reported, ERE's VaR on the book held): %d runs read "
      "an older EQX and FUTS extract when the feed failed, and neither of the %d exceptions on them (%s) is theirs, since "
      "ERE on the book held still falls short of each loss; every one of the %d runs from 1 July 2024 read extracts cut as "
      "it started, before the middle office booked the day's closing-auction allocations (a median USD %.1f million "
      "gross a night), which moved the VaR both ways (too high on %d runs) and caused the %d inputs exceptions, on %s."
      % (F["outage_runs"], len(F["outage_exceptions"]), dates(F["outage_exceptions"]), F["late_runs"],
         F["late_gross_median_m"], F["late_var_high_runs"], F["cutoff_caused"], dates(F["cutoff_dates"])))
    a("3. A sound model's count and zone, on a Sound model sheet with one row per day (hypothetical P&L, the sound "
      "model's VaR, exception): %d exceptions, on %s, the %s zone; %d to %d across decay 0.94 to 0.97 at the portfolio or "
      "name by name, green throughout."
      % (F["sound_count"], dates(F["sound_dates"]), F["sound_zone"].lower(), B["sound_count"][0], B["sound_count"][1]))
    a("4. The add-on on the planned book month by month, on an Add-on sheet with a bar chart (each month's planned mid "
      "and small cap gross, futures contracts, names ERE proxies, own-history VaR, ERE's VaR, add-on), USD million: %s."
      % "; ".join("%s %.2f (%.2f to %.2f)" % (mo[j], add[j], ab[j][0], ab[j][1]) for j in range(len(add))))
    a("5. A Summary sheet with the counts by heading and the corrected zone beside the official one, and a Routes sheet "
      "giving what each shortcut files beside the golden figure.")
    a("")
    a("### backtesting_note_2025Q2.pdf")
    a("")
    a("6. One page to the supervisor from the head of Market Risk Control: the corrected count against the official "
      "one, the heading table with its dates, a paragraph each on ERE's inputs and on the model, the add-on by month with "
      "the names proxied, and the actions (move ERE's extract after the allocation batch, fix the extract delivery, hold "
      "the add-on, bring the proxied names onto their own vendor history).")
    a("")
    a("## Critical Components")
    a("")
    a("1. There were **%d** exceptions, not %d: **%d** on hypothetical P&L that booked P&L hid (%s) and **%d** on booked "
      "P&L only (%s)." % (F["exceptions_total"], F["official_count"], F["hyp_only"], dates(F["hyp_only_dates"]),
                          F["booked_only"], dates(F["booked_only_dates"])))
    a("2. **%d** exceptions were caused by ERE's inputs, every one on a night its extract was cut before the closing "
      "allocations were booked (%s); the **%d** runs that read an older extract caused **none**."
      % (hc["inputs"], dates(F["cutoff_dates"]), F["outage_runs"]))
    a("3. **%d** exceptions are risks not in the model, the proxied names' own moves: %s." % (hc["omitted"], dates(hd["omitted"])))
    a("4. The add-on is **USD %.2f million** for July and falls to **nil** by December as ERE's proxied names fall from "
      "**%d** to **%d**." % (add[0], F["addon_proxied"][0], F["addon_proxied"][-1]))
    a("")
    a("## Step-by-Step")
    a("")
    a("1. From %s (latest version of each day) against the previous evening's completed run in %s: %d exceptions on "
      "booked P&L, as %s files them, %d on hypothetical P&L, %d in all (MRS-4 3.3)."
      % (FN["pc"], FN["runlog"], F["official_count"], FN["backtest"], F["hyp_count"], F["exceptions_total"]))
    a("2. Rebuilt ERE from %s on the extract each run read (%s and %s through %s, FUTS from %s, closes from %s keyed by "
      "vendor id): it matches all %d runs in the log to the dollar." % (FN["method"], FN["eqx1"], FN["eqx2"], FN["xwalk"],
                                                                       FN["futs"], FN["vendor"], F["runs_logged"]))
    a("3. The hurried reading stops there: the log's %d runs on an older extract, re-run on that day's extract, cover %d "
      "exceptions (%s), which it files under inputs, leaving %d under (c) and %d against the model."
      % (F["outage_runs"], len(F["careful_inputs_dates"]), dates(F["careful_inputs_dates"]),
         F["careful_heading_counts"]["omitted"], F["careful_model_count"]))
    a("4. Set each ticket's booking time in %s against each extract's cut: every evening the closing-auction "
      "allocations are booked after the cut, so the book held is the extract plus those bookings (the trades rolled "
      "forward from the first extract give the same book), and on it ERE covers the loss on %s and on neither "
      "reused night." % (FN["blotter"], dates(F["cutoff_dates"])))
    a("5. Re-ran MRS-4 4(c) and 4(d) on the book held with %s: own history covers %d more, the volatility-scaled VaR "
      "(decay 0.94, portfolio) %d, leaving %d to model accuracy." % (FN["vendor"], hc["omitted"], hc["volatility"],
                                                                     hc["sound"]))
    a("6. Counted the sound model over all 250 days (MRS-4 5): %d, green (%d to %d across the settings); with the "
      "proxies kept %d and with no volatility response %d." % (F["sound_count"], B["sound_count"][0], B["sound_count"][1],
                                                             sc["noprox"], sc["novol"]))
    a("7. Built each month's book from the 30 June run's extract by the basis in %s and priced it on the 30 June "
      "window and betas: July's add-on is USD %.2f million, against the 30 June add-on of %.2f scaled with gross (%.2f)."
      % (FN["plan"], add[0], F["addon_now_m"], F["addon_prop_m"][0]))
    a("8. Applied the note's 500-return rule to each name's store start in %s for the run that sets each month's first "
      "VaR (MRS-4 3.4 and 6): ERE proxies %s names from July to December and the add-on runs %s, where the 30 June "
      "mapping held under the plan's ramp gives %s." % (FN["mapping"], ", ".join(str(x) for x in F["addon_proxied"]),
                                                        ", ".join("%.2f" % x for x in add),
                                                        ", ".join("%.2f" % x for x in F["addon_ramp_only_m"])))
    a("")
    a("No other conclusion survives. The official count reads booked P&L alone and misses %d exceptions; blaming the "
      "reused extracts charges the model %d, because only the blotter's booking times show what each extract lacked; "
      "every allowed volatility setting keeps the sound count at %d to %d, green; and the add-on falls with the store's "
      "graduations whatever the ramp, so neither July's figure held flat nor the ramp alone (rising to %.2f) gives the "
      "months." % (F["hyp_only"], F["careful_model_count"], B["sound_count"][0], B["sound_count"][1],
                   F["addon_ramp_only_m"][-1]))
    a("")
    return "\n".join(L)
