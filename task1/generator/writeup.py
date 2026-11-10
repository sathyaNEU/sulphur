"""figures.json and submission.md, every figure emitted from the golden and the routes on the shipped pack (never
typed)."""
import numpy as np

import analysis as An
import golden as GD
import params as P

r10k, r100k = GD.r10k, GD.r100k


def c(x):
    return "{:,}".format(x)


def figures(F, B, g, R):
    raw, rounded, gap = GD.bridge(g)
    rl = F["raw_lines"]
    rt = F["raw_team"]
    months = [GD.label(m).strftime("%b %Y") for m in range(P.CUT + 1, P.HORIZON + 1)]
    kpi_sep = An.arr_at(F, P.CUT - 1)
    hur = {k: v for k, v in R.items() if v.get("kind") in ("hurried", "careful", "rival")}
    f = {
        "open_bus": r10k(g["open_bus"]), "open_team": r10k(g["open_team"]), "open_total": r10k(g["open_total"]),
        "price": r10k(g["price"]), "contraction": r10k(g["contraction"]), "churn": r10k(g["churn"]),
        "expansion_bridge": dict(rounded)["Business seat additions"],
        "team_change": dict(rounded)["Change in Team"],
        "new_bus": r10k(g["new_bus"]), "new_open": r10k(g["new_open"]), "new_future": r10k(g["new_bus"]) - r10k(g["new_open"]) - r10k(g["new_upgrade"]),
        "new_upgrade": r10k(g["new_upgrade"]), "team_left": r10k(g["team_left"]), "team_new": r10k(g["team_new"]),
        "dec27": r10k(g["dec27"]), "p10": r10k(g["p10"]), "p90": r10k(g["p90"]), "p20": r10k(g["p20"]),
        "commitment": r100k(g["p20"]), "draft": GD.DRAFT,
        "draft_verdict": "no" if r100k(g["p20"]) < GD.DRAFT else "yes",
        "draft_chance_pct": int(round(100 * np.mean(np.array(g["draws"]) >= GD.DRAFT * 1e6))),
        "bridge": {k: v for k, v in rounded},
        "bridge_gap": gap,
        "path_months": months,
        "path": [r10k(x) for x in g["path"]],
        "path_p10": [r10k(x) for x in g["path_p10"]],
        "path_p90": [r10k(x) for x in g["path_p90"]],
        "uplift_at_20": round(float(g["uplift_fit"][1]), 3),
        "uplift_share_pct": int(round(100 * g["uplift_fit"][1] / (P.BUS_LIST_NEW["EUR"] / P.BUS_LIST_OLD["EUR"] - 1))),
        "uplift_mean": round(An.fit_business(B.E)["uplift_mean"], 3),
        "renewals_used": int(len(B.E)),
        "repricings": int(An.fit_business(B.E)["uplift_n"]),
        "team_persist": round(g["team_persist"], 4),
        "team_persist_pts": round(100 * g["team_persist"], 1),
        "kpi_sep_total": r10k(kpi_sep[0] + kpi_sep[1]),
        "lines_raw": int(len(rl)), "lines_dup": int(rl.duplicated().sum()),
        "lines_credited": int((rl["line_type"] == "Credit note").sum()),
        "team_failed": int((rt["status"] != "paid").sum()),
        "open_deals": int((B.S["m"] == P.CUT).sum()),
        "plan_rate": P.PLAN_RATE_GBP,
        "conventions": {"policy_sections": [2.1, 2.2, 2.3, 2.4, 4.1, 4.3, 4.4, 4.5, 4.6], "pct": [10, 20, 80, 90],
                        "rounding": [10000, 0.1], "per": 100, "first_renewal": 1, "list_rise_pct": 26.7, "seats_ref": 20,
                        "team_min_seats": 3, "months": 14, "drift_windows": [12, 18, 24]},
    }
    for k, v in hur.items():
        f["route_" + k.replace(" ", "_").replace("'", "")] = {
            "price": r10k(v["price"]), "contraction": r10k(v["contraction"]), "churn": r10k(v["churn"]),
            "team_left": r10k(v["team_left"]), "new_open": r10k(v["new_open"]), "new_bus": r10k(v["new_bus"]),
            "dec27": r10k(v["dec27"]), "p20": r10k(v["p20"]), "commitment": r100k(v["p20"])}
    f["opening"] = {"business": f["open_bus"], "team": f["open_team"]}
    f["renewal_lines"] = {"contraction": f["contraction"], "churn": f["churn"]}
    f["new_split"] = {"new_bus": f["new_bus"], "new_open": f["new_open"]}
    f["path_table"] = dict(zip(f["path_months"], f["path"]))
    fam = [g] + [v for v in R.values() if v.get("kind") == "rival"]
    for k in ("price", "contraction", "churn", "team_left", "new_open", "new_bus", "dec27", "p10", "p90"):
        f["band_" + k] = [min(r10k(x[k]) for x in fam), max(r10k(x[k]) for x in fam)]
    f["band_path"] = [[min(r10k(x["path"][i]) for x in fam), max(r10k(x["path"][i]) for x in fam)]
                      for i in range(len(months))]
    riv = [r100k(v["p20"]) for v in R.values() if v.get("kind") == "rival"] + [f["commitment"]]
    f["commitment_lo"], f["commitment_hi"] = min(riv), max(riv)
    f["reps"] = 2000
    f["quick_dec27"] = r10k(R["quick"]["dec27"])
    f["quick_commitment"] = r100k(R["quick"]["dec27"])
    f["quick_growth_pct"] = round(100 * (R["quick"]["growth12"] - 1), 1)
    # the hurried assembly: every subscription line in force summed as exported, failed Team invoices kept
    f["r1_all_lines"] = r10k(all_lines_arr(F))
    f["r1_team_all_rows"] = r10k(team_all_rows(F))
    return f


def all_lines_arr(F):
    """Business ARR with every subscription and true-up line in force summed as exported (re-exported duplicates,
    credited lines and credit notes all kept)."""
    import pandas as pd
    L = F["raw_lines"]
    s = pd.to_datetime(L["service_start"])
    e = pd.to_datetime(L["service_end"])
    cut = pd.Timestamp(2026, 10, 31)
    x = L[(s <= cut) & (e >= cut) & L["line_type"].isin(["Subscription - new", "Subscription - renewal",
                                                            "Seat true-up", "Credit note"])]
    fx = x["currency"].map({"EUR": 1.0, "GBP": P.PLAN_RATE_GBP})
    return float((x["quantity"] * x["unit_price"] * 12 * fx).sum())


def team_all_rows(F):
    import pandas as pd
    T = F["raw_team"]
    s = pd.to_datetime(T["period_start"])
    e = pd.to_datetime(T["period_end"])
    cut = pd.Timestamp(2026, 10, 31)
    x = T[(s <= cut) & (e >= cut)]
    fx = x["currency"].map({"EUR": 1.0, "GBP": P.PLAN_RATE_GBP})
    return float((x["seats_billed"] * x["price_per_seat"] * 12 * fx).sum())


def write(path, f):
    rt = lambda k: f["route_" + k.replace(" ", "_").replace("'", "")]
    flat, lst = rt("mean uplift applied flat"), rt("list rise applied flat")
    pooled, indep = rt("pooled renewal rates"), rt("accounts drawn independently")
    since, t12 = rt("Team rates since April"), rt("Team rates of the trailing twelve months")
    crm, runr, stage = rt("CRM stage probabilities"), rt("trailing run-rate of new ARR"), rt("win odds by stage alone")
    car = rt("careful but hurried")
    b = f["bridge"]
    E = lambda x: "EUR " + c(x)

    def band(k):
        lo, hi = f["band_" + k]
        return "" if lo == hi else " (the defensible methods give %s to %s)" % (E(lo), E(hi))
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Product Analytics, Cohort and LTV modeling (retention curves, customer lifetime value).")
    L.append("**Task type:** forecast of a seat-licensed SaaS book's December 2027 ARR, built flow by flow, with an "
             "80 per cent band and a bridge.")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## Final Recommendation\n")
    L.append("**Commit EUR %.1f million of December 2027 ARR in the 2027 plan, not the draft's EUR %.1f million**: "
             "December 2027 ARR has an 80 per cent chance of reaching %s (expected %s, 80 per cent range %s to %s), "
             "and the draft is met only about %d times in 100. A forecast that applies the average price rise to "
             "every renewal, pools renewal rates, values the pipeline at the CRM's stage probabilities and draws "
             "accounts independently puts the 80 per cent figure at EUR %.1f million and wrongly clears the draft.\n"
             % (f["commitment"], f["draft"], E(f["p20"]), E(f["dec27"]), E(f["p10"]), E(f["p90"]),
                f["draft_chance_pct"], car["commitment"]))
    L.append("## Supplementary Questions\n")
    L.append("### arr_2027_forecast.xlsx\n")
    path_txt = "; ".join("%s %s (%s to %s)" % (m, c(v), c(lo), c(hi)) for m, v, lo, hi in
                     zip(f["path_months"], f["path"], f["path_p10"], f["path_p90"]))
    L.append("1. Sheet Forecast: one row per month end from October 2026 (on the books, %s) to December 2027, "
             "columns month end, expected ARR, 80 per cent range low (10th percentile) and high (90th percentile), "
             "EUR to the nearest 10,000: %s. Below it the December 2027 summary: expected %s, P10 %s, P90 %s, the "
             "80 per cent figure %s, commitment EUR %.1f million, draft EUR %.1f million, draft clears: No."
             % (c(f["open_total"]), path_txt, c(f["dec27"]), c(f["p10"]), c(f["p90"]), c(f["p20"]), f["commitment"],
                f["draft"]))
    L.append("2. Sheet Bridge: ARR 31 October 2026 %s; new Business %s; Business seat additions %s; price %s; "
             "Business seat reductions %s; Business accounts lost %s; change in Team %s; expected ARR 31 December "
             "2027 %s, the lines adding up exactly at the nearest EUR 10,000. Under it the new Business split (open "
             "deals %s, deals created from November 2026 %s, Team accounts moving to Business %s) and the Team split "
             "(accounts on Team at 31 October 2026 %s, Team accounts signing from November 2026 %s). Further sheets "
             "list the inputs and what each shortcut gives.\n"
             % (E(f["open_total"]), E(b["New Business"]), E(b["Business seat additions"]), E(b["Price"]),
                "-" + E(-b["Business seat reductions"]), "-" + E(-b["Business accounts lost"]),
                E(b["Change in Team"]), E(f["dec27"]), E(f["new_open"]), E(f["new_future"]), E(f["new_upgrade"]),
                E(f["team_left"]), E(f["team_new"])))
    L.append("### arr_2027_note.docx\n")
    L.append("3. The call: commit EUR %.1f million (the 80 per cent figure is %s); the draft's EUR %.1f million does "
             "not clear the 80 per cent bar (met about %d times in 100)." % (f["commitment"], E(f["p20"]), f["draft"],
                                                                            f["draft_chance_pct"]))
    L.append("4. ARR on the books at 31 October 2026: Business %s, Team %s (total %s)." %
             (E(f["open_bus"]), E(f["open_team"]), E(f["open_total"])))
    L.append("5. Team ARR in December 2027 from accounts already on the Team plan at 31 October 2026: %s%s." %
             (E(f["team_left"]), band("team_left")))
    L.append("6. New Business ARR signed November 2026 to December 2027 from deals open at 31 October 2026: %s%s (of "
             "%s new Business in all).\n" % (E(f["new_open"]), band("new_open"), E(f["new_bus"])))
    L.append("## Critical Components\n")
    L.append("1. The price line is **%s**%s: the realised uplift at renewal falls with contract size (about %d per "
             "cent of the list rise at 20 seats), so the average uplift applied flat (%s) or the list rise (%s) "
             "overstates it." % (E(f["price"]), band("price"), f["uplift_share_pct"], E(flat["price"]),
                                 E(lst["price"])))
    L.append("2. Business seat reductions are **%s**%s and Business accounts lost **%s**%s, from a renewal model on "
             "utilisation (workspace activity through the dated links), first renewals and group exits; pooled rates "
             "give seat reductions of %s." % (E(f["contraction"]), band("contraction"), E(f["churn"]), band("churn"),
                                             E(pooled["contraction"])))
    L.append("3. New Business is **%s**%s, of which **%s**%s from deals open at 31 October 2026, on win odds by stage "
             "and time in stage; the CRM's stage probabilities value the open deals at %s." %
             (E(f["new_bus"]), band("new_bus"), E(f["new_open"]), band("new_open"), E(crm["new_open"])))
    L.append("4. December 2027 ARR has an 80 per cent range of **%s to %s** and an 80 per cent figure of **%s** "
             "(commitment EUR %.1f million; the defensible methods give EUR %.1f to %.1f million) with a parent "
             "group's accounts drawn together; drawn independently the figure is %s." %
             (E(f["p10"]), E(f["p90"]), E(f["p20"]), f["commitment"], f["commitment_lo"], f["commitment_hi"],
              E(indep["p20"])))
    L.append("")
    L.append("## Step-by-Step\n")
    st = [
        "Opening book (billing_contract_lines_2022-01_2026-10.csv, team_invoices_2022-01_2026-10.csv): re-exported "
        "lines counted once, credited lines replaced by their re-issues, onboarding fees and part-term true-up charges "
        "left out, failed card payments dropped, GBP at the plan rate (policy 2): Business %s and Team %s at 31 "
        "October 2026; September's figure reproduces the KPI export (%s). Summing every exported line gives %s for "
        "Business." % (E(f["open_bus"]), E(f["open_team"]), E(f["kpi_sep_total"]), E(f["r1_all_lines"])),
        "Price: from the %d repricings since 1 March 2026, the per-seat price change at renewal fitted on log seats "
        "(%d per cent of the list rise at 20 seats, less on larger contracts) and applied to each contract still to "
        "reprice: %s. The mean uplift applied flat gives %s, the list rise %s." %
        (f["repricings"], f["uplift_share_pct"], E(f["price"]), E(flat["price"]), E(lst["price"])),
        "Renewals: workspace activity joined to accounts through workspace_account_links.csv on the dated links, "
        "utilisation at each of the %s renewals since 2022, CRM parent groups from crm_accounts_export_2026-11-02.xlsx; "
        "exits modelled on utilisation, first renewal and a sibling's recent exit, seat cuts on utilisation and "
        "renewal number: seat reductions %s, accounts lost %s. Pooled rates give %s and %s." %
        (c(f["renewals_used"]), E(f["contraction"]), E(f["churn"]), E(pooled["contraction"]), E(pooled["churn"])),
        "Seat additions: each account's own drift in active users projected against its seats, true-ups when users "
        "pass seats: %s in the bridge." % E(f["expansion_bridge"]),
        "Team: monthly exit rates by members and age before April 2026, plus the excess on the accounts padded to "
        "three seats, which fell month by month to a lasting %.1f points a month; December 2027 Team ARR from "
        "the October accounts %s. Reading the months since April as the new rate gives %s, the trailing twelve months %s." %
        (f["team_persist_pts"], E(f["team_left"]), E(since["team_left"]), E(t12["team_left"])),
        "Pipeline (pipeline_snapshots_2023-01_2026-10.csv, opportunities_closed_2022-01_2026-10.csv): re-run snapshot "
        "rows once, monthly amounts set aside for quoted seats priced at won deals' first contracts, win timing by "
        "stage and months in stage from snapshots with a full 14-month follow-up: open deals %s, all new Business %s. "
        "The CRM's probabilities give %s and %s; stage alone %s; the trailing run-rate of new ARR %s." %
        (E(f["new_open"]), E(f["new_bus"]), E(crm["new_open"]), E(crm["new_bus"]), E(stage["new_open"]),
         E(runr["new_bus"])),
        "Band: %d simulated paths with each parent group's exits feeding its siblings' next renewals and new deals "
        "drawn as whole deals: P10 %s, P20 %s, P90 %s. Independent draws give a P20 of %s." %
        (f["reps"], E(f["p10"]), E(f["p20"]), E(f["p90"]), E(indep["p20"])),
        "Path and bridge: the monthly expected path and its range from the same paths, the six lines in the "
        "policy's order adding from %s to %s; commitment EUR %.1f million, below the draft." %
        (E(f["open_total"]), E(f["dec27"]), f["commitment"]),
    ]
    for i, s in enumerate(st, 1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("No other figure survives the files. Carrying the last twelve months' growth forward (%s a year) gives "
             "%s; the shortcuts taken together (flat uplift, pooled renewals, the last three months' Team rates, CRM "
             "probabilities, independent draws) give a commitment of EUR %.1f million; each is ruled out by the "
             "repricings' size gradient, the renewals' utilisation and group pattern, the decline in the April "
             "excess and the closed deals' history. The rivals a careful analyst can defend (uplift by size band, "
             "utilisation in bins or left out of the exit model, the April excess from two months or an exponential, "
             "win odds by stage and deal age, seat additions from 12 or 18 months of drift, each account's own "
             "trailing rate or the book's trailing rate at accounts near their seats) all keep the commitment at EUR %.1f to %.1f million, below the draft."
             % ("%.1f per cent" % f["quick_growth_pct"], E(f["quick_dec27"]), car["commitment"], f["commitment_lo"],
                f["commitment_hi"]))
    open(path, "w").write("\n".join(L) + "\n")
