"""figures.json and submission.md, every figure emitted from the golden and the routes on the shipped pack (never
typed)."""
import numpy as np

import analysis as An
import golden as GD
import params as P
import routes as RT

r10k, r100k, r50k, commit_m, rk, ROUND, UNIT_WORD = GD.r10k, GD.r100k, GD.r50k, GD.commit_m, GD.rk, GD.ROUND, GD.UNIT_WORD


def c(x):
    return "{:,}".format(x)


def figures(F, B, g, R):
    raw, rounded, gap = GD.bridge(g)
    rl = F["raw_lines"]
    rt = F["raw_team"]
    months = [GD.label(m).strftime("%b %Y") for m in range(P.CUT + 1, P.HORIZON + 1)]
    kpi_sep = An.arr_at(F, P.CUT - 1)
    hur = {k: v for k, v in R.items() if v.get("kind") in ("hurried", "careful", "rival")}
    draws = np.array(g["draws"])
    f = {
        "open_bus": r10k(g["open_bus"]), "open_team": r10k(g["open_team"]), "open_total": r10k(g["open_total"]),
        "price": r10k(g["price"]), "contraction": rk("contraction")(g["contraction"]), "churn": rk("churn")(g["churn"]),
        "contraction_10k": r10k(g["contraction"]), "churn_10k": r10k(g["churn"]),
        "expansion_bridge": dict(rounded)["Business seat additions"],
        "team_change": dict(rounded)["Change in Team"],
        "new_bus": r10k(g["new_bus"]), "new_open": rk("new_open")(g["new_open"]),
        "new_upgrade": r10k(g["new_upgrade"]), "team_left": rk("team_left")(g["team_left"]), "team_new": r10k(g["team_new"]),
        "dec27": r10k(g["dec27"]), "p10": r10k(g["p10"]), "p90": r10k(g["p90"]), "p20": r10k(g["p20"]),
        "commitment": commit_m(g), "commitment_met_pct": int(round(100 * g["commitment_met"])),
        "commitment_next": round(commit_m(g) + 0.1, 1),
        "commitment_next_met_pct": int(round(100 * g["commitment_next_met"])),
        "draft": GD.DRAFT,
        "draft_verdict": "no" if commit_m(g) < GD.DRAFT else "yes",
        "draft_chance_pct": int(round(100 * np.mean(draws >= GD.DRAFT * 1e6))),
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
        "season_high_pct": int(round(100 * (max(g["team_season"].values()) - 1))),
        "season_low_pct": int(round(100 * (1 - min(g["team_season"].values())))),
        "kpi_sep_total": r10k(kpi_sep[0] + kpi_sep[1]),
        "lines_raw": int(len(rl)), "lines_dup": int(rl.duplicated().sum()),
        "lines_credited": int((rl["line_type"] == "Credit note").sum()),
        "team_failed": int((rt["status"] != "paid").sum()),
        "open_deals": int((B.S["m"] == P.CUT).sum()),
        "plan_rate": P.PLAN_RATE_GBP,
        "conventions": {"policy_sections": [2.1, 2.2, 2.3, 2.4, 4.1, 4.3, 4.4, 4.5, 4.6, 5.2, 5.3], "pct": [10, 20, 80, 90],
                        "rounding": [10000, 50000, 100000, 0.1], "per": 100, "first_renewal": 1, "list_rise_pct": 26.7,
                        "precision": {k: int(v) for k, v in ROUND.items()},
                        "seats_ref": 20, "team_min_seats": 3, "months": 14, "drift_windows": [12, 18, 24],
                        "common_factor": 0.25, "price_rise_month": 1, "team_min_month": 1},
    }
    for k, v in hur.items():
        f["route_" + k.replace(" ", "_").replace("'", "")] = {
            "price": r10k(v["price"]), "contraction": rk("contraction")(v["contraction"]), "churn": rk("churn")(v["churn"]),
            "contraction_10k": r10k(v["contraction"]), "churn_10k": r10k(v["churn"]),
            "team_left": rk("team_left")(v["team_left"]), "new_open": rk("new_open")(v["new_open"]), "new_bus": r10k(v["new_bus"]),
            "dec27": r10k(v["dec27"]), "p20": r10k(v["p20"]), "p10": r10k(v["p10"]), "p90": r10k(v["p90"]),
            "commitment": commit_m(v)}
    f["naive"] = {k: r10k(v) for k, v in R["naive"].items() if k != "kind"}
    f["naive_min"] = min(f["naive"].values())
    f["opening"] = {"business": f["open_bus"], "team": f["open_team"]}
    f["renewal_lines"] = {"contraction": f["contraction"], "churn": f["churn"]}
    f["new_split"] = {"new_bus": f["new_bus"], "new_open": f["new_open"]}
    f["path_table"] = dict(zip(f["path_months"], f["path"]))
    fam = [g] + [v for v in R.values() if v.get("kind") == "rival"]
    for k, rd in (("price", r10k), ("contraction", rk("contraction")), ("churn", rk("churn")), ("team_left", rk("team_left")),
                  ("new_open", rk("new_open")), ("new_bus", r10k), ("dec27", r10k), ("p10", r10k), ("p90", r10k)):
        f["band_" + k] = [min(rd(x[k]) for x in fam), max(rd(x[k]) for x in fam)]
    f["band_path"] = [[min(r10k(x["path"][i]) for x in fam), max(r10k(x["path"][i]) for x in fam)]
                      for i in range(len(months))]
    riv = [commit_m(v) for v in R.values() if v.get("kind") == "rival"] + [f["commitment"]]
    f["commitment_lo"], f["commitment_hi"] = min(riv), max(riv)
    f["reps"] = RT.REPS
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
    since, t12, l3 = rt("Team rates since April"), rt("Team rates of the trailing twelve months"), \
        rt("Team rates of the last three months")
    crm, runr, stage = rt("CRM stage probabilities"), rt("trailing run-rate of new ARR"), rt("win odds by stage alone")
    common, nop = rt("an assumed common factor of 0.25 added"), rt("band without the estimation uncertainty")
    car = rt("careful but hurried")
    b = f["bridge"]
    nv = f["naive"]
    E = lambda x: "EUR " + c(x)
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Product Analytics, Cohort and LTV modeling (retention curves, customer lifetime value).")
    L.append("**Task type:** forecast of a seat-licensed SaaS book's December 2027 ARR, built flow by flow, with an "
             "80 per cent band, a bridge and the commitment the board can be given.")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## Final Recommendation\n")
    L.append("**Commit EUR %.1f million of December 2027 ARR in the 2027 plan, not the draft's EUR %.1f million**: "
             "EUR %.1f million is the largest EUR 0.1 million step met or beaten in at least 80 per cent of outcomes "
             "(%d in 100; EUR %.1f million only %d in 100), the draft is met about %d times in 100, and expected ARR "
             "is %s with an 80 per cent range of %s to %s. Every trailing extrapolation clears the draft (the last "
             "twelve months carried forward give %s to %s), and a forecast that applies the average price rise to "
             "the remaining renewals, pools renewal rates, carries the Team plan's last three months, values the "
             "pipeline at the CRM's stage probabilities and draws accounts independently puts the commitment at "
             "EUR %.1f million; the flows the files carry do not get there.\n"
             % (f["commitment"], f["draft"], f["commitment"], f["commitment_met_pct"], f["commitment_next"],
                f["commitment_next_met_pct"], f["draft_chance_pct"], E(f["dec27"]), E(f["p10"]), E(f["p90"]),
                E(nv["trailing twelve months' net new ARR carried forward"]),
                E(nv["trailing twelve months' growth compounded"]), car["commitment"]))
    L.append("## Supplementary Questions\n")
    L.append("### arr_2027_forecast.xlsx\n")
    path_txt = "; ".join("%s %s (%s to %s)" % (m, c(v), c(lo), c(hi)) for m, v, lo, hi in
                         zip(f["path_months"], f["path"], f["path_p10"], f["path_p90"]))
    L.append("1. Sheet Forecast: one row per month end from October 2026 (on the books, %s) to December 2027, "
             "columns month end, expected ARR, 80 per cent range low (10th percentile) and high (90th percentile), "
             "EUR to the nearest 10,000: %s. Below it the December 2027 summary: expected %s, P10 %s, P90 %s, "
             "20th percentile %s, commitment EUR %.1f million (met in %d of 100 outcomes; EUR %.1f million in %d), "
             "draft EUR %.1f million (met in %d of 100), draft clears: No."
             % (c(f["open_total"]), path_txt, c(f["dec27"]), c(f["p10"]), c(f["p90"]), c(f["p20"]), f["commitment"],
                f["commitment_met_pct"], f["commitment_next"], f["commitment_next_met_pct"], f["draft"],
                f["draft_chance_pct"]))
    L.append("2. Sheet Bridge: ARR 31 October 2026 %s; new Business %s; Business seat additions %s; price %s; "
             "Business seat reductions %s; Business accounts lost %s; change in Team %s; expected ARR 31 December "
             "2027 %s, the lines adding up exactly at the nearest EUR 10,000. Further sheets list the inputs, what "
             "each shortcut gives and what each trailing extrapolation gives.\n"
             % (E(f["open_total"]), E(b["New Business"]), E(b["Business seat additions"]), E(b["Price"]),
                "-" + E(-b["Business seat reductions"]), "-" + E(-b["Business accounts lost"]),
                E(b["Change in Team"]), E(f["dec27"])))
    L.append("### arr_2027_note.docx\n")
    L.append("3. The call: commit EUR %.1f million, the largest EUR 0.1 million step met or beaten in at least 80 per "
             "cent of outcomes (%d in 100); the draft's EUR %.1f million does not clear the bar (met about %d times "
             "in 100)." % (f["commitment"], f["commitment_met_pct"], f["draft"], f["draft_chance_pct"]))
    L.append("4. ARR on the books at 31 October 2026: Business %s, Team %s (total %s)." %
             (E(f["open_bus"]), E(f["open_team"]), E(f["open_total"])))
    L.append("5. Team ARR in December 2027 from accounts already on the Team plan at 31 October 2026: %s (to the "
             "%s)." % (E(f["team_left"]), UNIT_WORD[ROUND["team_left"]]))
    L.append("6. New Business ARR signed November 2026 to December 2027 from deals open at 31 October 2026: %s (to "
             "the %s), of %s new Business in all.\n" % (E(f["new_open"]), UNIT_WORD[ROUND["new_open"]], E(f["new_bus"])))
    L.append("## Critical Components\n")
    L.append("1. The price line is **%s** (nearest EUR 10,000): the realised uplift at renewal falls with contract "
             "size (about %d per cent of the list rise at 20 seats), so the average realised uplift applied flat "
             "(%s) or the list rise (%s) overstates what the November and December renewals still bring."
             % (E(f["price"]), f["uplift_share_pct"], E(flat["price"]), E(lst["price"])))
    L.append("2. Business seat reductions are **%s** (%s) and Business accounts lost **%s** (%s), from a renewal "
             "model on utilisation (workspace activity through the dated links), first renewals and group exits; "
             "pooled renewal rates put accounts lost at %s and drawing accounts independently of their group at %s."
             % (E(f["contraction"]), UNIT_WORD[ROUND["contraction"]], E(f["churn"]), UNIT_WORD[ROUND["churn"]],
                E(pooled["churn"]), E(indep["churn"])))
    L.append("3. New Business is **%s** (nearest EUR 10,000), of which **%s** (%s) from deals open at "
             "31 October 2026, on win odds by stage and time in stage; the CRM's stage probabilities value the open "
             "deals at %s." % (E(f["new_bus"]), E(f["new_open"]), UNIT_WORD[ROUND["new_open"]], E(crm["new_open"])))
    L.append("4. The Team accounts on the plan at 31 October 2026 bring **%s** (%s) in December 2027, "
             "on the calendar pattern of cancellations (the autumn months about %d per cent above the year's "
             "average) and the January minimum's excess exits, now faded to %.1f points a month; %s."
             % (E(f["team_left"]), UNIT_WORD[ROUND["team_left"]], f["season_high_pct"], f["team_persist_pts"],
                ("the last three months carried forward, and the months since January, both give %s" % E(l3["team_left"]))
                if l3["team_left"] == since["team_left"] else
                ("the last three months carried forward give %s and the months since January %s"
                 % (E(l3["team_left"]), E(since["team_left"])))))
    L.append("5. The commitment is **EUR %.1f million**: the 80 per cent range %s to %s carries the accounts' and "
             "deals' outcomes with each estimated rate redrawn from its own sampling error (policy 5.2); without the "
             "estimation uncertainty the commitment is the same step (20th percentile %s against %s), and an assumed "
             "common factor of 0.25 across accounts, which the policy rules out, widens the range to %s to %s."
             % (f["commitment"], E(f["p10"]), E(f["p90"]), E(f["p20"]), E(nop["p20"]), E(common["p10"]),
                E(common["p90"])))
    L.append("")
    L.append("## Step-by-Step\n")
    st = [
        "Opening book (billing_contract_lines_2022-01_2026-10.csv, team_invoices_2022-01_2026-10.csv): re-exported "
        "lines counted once, credited lines replaced by their re-issues, onboarding fees and part-term true-up charges "
        "left out, failed card payments dropped, GBP at the plan rate (policy 2): Business %s and Team %s at 31 "
        "October 2026; September's figure reproduces the KPI export (%s). Summing every exported line gives %s for "
        "Business." % (E(f["open_bus"]), E(f["open_team"]), E(f["kpi_sep_total"]), E(f["r1_all_lines"])),
        "Trailing extrapolations, for the record: the last twelve months' net new ARR carried forward gives %s, "
        "compounded %s, the last six months %s; all clear the draft, and all carry the January 2026 price rise, "
        "which has landed on every contract except those renewing in November and December."
        % (E(nv["trailing twelve months' net new ARR carried forward"]), E(nv["trailing twelve months' growth compounded"]),
           E(nv["trailing six months' net new ARR carried forward"])),
        "Price: from the %d repricings since 1 January 2026, the per-seat price change at renewal fitted on log seats "
        "(%d per cent of the list rise at 20 seats, less on larger contracts) and applied to each contract still to "
        "reprice: %s. The mean uplift applied flat gives %s, the list rise %s." %
        (f["repricings"], f["uplift_share_pct"], E(f["price"]), E(flat["price"]), E(lst["price"])),
        "Renewals: workspace activity joined to accounts through workspace_account_links.csv on the dated links, "
        "utilisation at each of the %s renewals since 2022, CRM parent groups from crm_accounts_export_2026-11-02.xlsx; "
        "exits modelled on utilisation, first renewal and a sibling's recent exit, seat cuts on utilisation and "
        "renewal number, the accounts signed in the last two years carrying more seats per working user than the "
        "older book: seat reductions %s (%s), accounts lost %s (%s); %s and %s in the bridge. Pooled rates "
        "give %s and %s; drawing accounts independently of their group %s lost." %
        (c(f["renewals_used"]), E(f["contraction"]), UNIT_WORD[ROUND["contraction"]], E(f["churn"]),
         UNIT_WORD[ROUND["churn"]], E(f["contraction_10k"]), E(f["churn_10k"]),
         E(pooled["contraction"]), E(pooled["churn"]), E(indep["churn"])),
        "Seat additions: each account's own drift in active users projected against its seats, true-ups when users "
        "pass seats: %s in the bridge." % E(f["expansion_bridge"]),
        "Team: monthly exit rates by members and age from the history before January 2026 with a calendar index of "
        "cancellations (autumn about %d per cent above the year's average, late winter %d per cent below), plus the "
        "excess on the accounts padded to three seats, which fell month by month to a lasting %.1f points a month; "
        "December 2027 Team ARR from the October accounts %s. %s; the pre-January rates with no excess give %s." %
        (f["season_high_pct"], f["season_low_pct"], f["team_persist_pts"], E(f["team_left"]),
         ("The last three months carried forward, the months since January and the trailing twelve months all give %s"
          % E(l3["team_left"])) if l3["team_left"] == since["team_left"] == t12["team_left"] else
         ("The last three months carried forward give %s, the months since January %s, the trailing twelve months %s"
          % (E(l3["team_left"]), E(since["team_left"]), E(t12["team_left"]))),
         E(rt("Team rates before April")["team_left"])),
        "Pipeline (pipeline_snapshots_2023-01_2026-10.csv, opportunities_closed_2022-01_2026-10.csv): re-run snapshot "
        "rows once, monthly amounts set aside for quoted seats priced at won deals' first contracts, win timing by "
        "stage and months in stage from snapshots with a full 14-month follow-up, deals not yet created at the "
        "trailing twelve months' creation rate: open deals %s, all new Business %s. The CRM's probabilities give %s "
        "and %s." % (E(f["new_open"]), E(f["new_bus"]), E(crm["new_open"]), E(crm["new_bus"])),
        "Band: %d simulated paths, each with every estimated rate redrawn from its sampling error and each parent "
        "group's exits feeding its siblings' next renewals, new deals and sign-ups drawn as whole deals and teams: "
        "P10 %s, 20th percentile %s, P90 %s; the largest EUR 0.1 million step met in at least 80 per cent of the "
        "paths is EUR %.1f million (%d in 100). Without the estimation uncertainty the step is the same (20th "
        "percentile %s); an added common factor of 0.25, which policy 5.2 rules out, widens the range to %s to %s; "
        "independent draws give EUR %.1f million." %
        (f["reps"], E(f["p10"]), E(f["p20"]), E(f["p90"]), f["commitment"], f["commitment_met_pct"], E(nop["p20"]),
         E(common["p10"]), E(common["p90"]), indep["commitment"]),
        "Path and bridge: the monthly expected path and its range from the same paths, the six lines in the "
        "policy's order adding from %s to %s; the draft's EUR %.1f million is met in %d of 100 paths and does not "
        "clear the bar." % (E(f["open_total"]), E(f["dec27"]), f["draft"], f["draft_chance_pct"]),
    ]
    for i, s in enumerate(st, 1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("No other figure survives the files. The trailing views (%s to %s) clear the draft because they carry "
             "the January price rise and the Team minimum's padded seats as if they recurred; the shortcuts taken "
             "together (flat uplift, pooled renewals, the last three months' Team rates, CRM probabilities, "
             "independent draws) give a commitment of EUR %.1f million; each is ruled out by the repricings' size "
             "gradient, the renewals' utilisation and group pattern, the calendar pattern and the decline of the "
             "January excess on the Team plan, the closed deals' history and policy 5.2 on what the range carries. "
             "The rivals a careful analyst can defend (uplift by size band, utilisation in bins, the January excess "
             "from two months or an exponential, the calendar index by quarter or smoothed, utilisation in bins or left "
             "out of the exit model, win odds by stage and deal age, deal creation over eighteen months, seat additions "
             "from 12 or 18 months of drift or each account's own trailing rate) all land on EUR %.1f million."
             % (E(f["naive_min"]), E(nv["trailing twelve months' growth compounded"]), car["commitment"],
                f["commitment"]))
    open(path, "w").write("\n".join(L) + "\n")
