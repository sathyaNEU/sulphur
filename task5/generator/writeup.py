"""task5 architecture 4: generator/figures.json and submission.md, written from the golden's own objects.

Every number the four answer blocks state passes through Rec.f(), which files it in figures.json under a key and
returns it formatted, so no figure is typed. The effort test's results (effort_passes.py) are tied to the r*_ keys."""
import json
import os

import golden as GD
import methods as M
import world as W


class Rec:
    def __init__(self):
        self.d = {}

    def f(self, key, value, fmt="{:,}"):
        self.d[key] = value
        return fmt.format(value)


def names(codes):
    n = [W.NAMES[c] for c in codes]
    if not n:
        return "no county"
    return n[0] if len(n) == 1 else ", ".join(n[:-1]) + " and " + n[-1]


def listed(parts):
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def r2_value(counts, keep):
    return dict(batch_not_arrived=counts["batch"], on_its_own=counts["alone"], late_every_quarter=counts["habit"],
                two_quarters=counts["twoq"], new_account=counts["new"], on_its_own_keep=round(keep, 2))


def figures_and_blocks(pk, G, n):
    R = Rec()
    f = R.f
    B = G["bands"]
    cz, rc, ui, tr, rp, st = G["census"], G["recon"], G["uinfo"], G["trouble"], G["replay"], G["sites"]
    des = G["designated"]
    ch = G["change"]
    near = sorted([c for c in W.CODES if c not in des], key=lambda c: ch[c])[0]
    route = dict(zip(M.SHORTCUT_KEYS, G["routes"]))
    careful, surv, kept, rep_all = route["careful"], route["pooled_surv"], route["pooled_kept"], route["pooled_rep"]
    noB, latest, level = route["no_unreg"], route["latest"], route["level"]
    pc1, pc2 = "{:.1f}", "{:.2f}"
    lm = G["latest_minus_site"]
    worst = [c for c in W.CODES if abs(lm[c]) >= 60]
    gain = sorted([c for c in worst if lm[c] > 0], key=lambda c: -lm[c])
    lose = sorted([c for c in worst if lm[c] < 0], key=lambda c: lm[c])
    # ---- the effort test's keys (the same objects the blocks state)
    R.d["r1_census_and_reconciliation"] = dict(liable=cz["liable"], received=cz["received"], outstanding=cz["outstanding"],
                                               published=rc["published"], now=rc["now"], late_reports=rc["late_jobs"],
                                               accounts_since=rc["new_jobs"], amendments=rc["amend_jobs"])
    R.d["r2_outstanding_by_cause"] = r2_value({k: G["kinds"][k]["n"] for k in GD.KIND_ORDER}, G["k_alone"])
    R.d["r3_this_quarter"] = dict(construction_share=round(100 * tr[15]["constr"], 1),
                                  a_year_earlier=round(100 * tr[11]["constr"], 1))
    R.d["r4_unregistered"] = dict(employers=int(round(ui["n"], -1)), jobs=GD.r100(G["unreg_jobs"]))
    R.d["r5_worksite_split"] = {W.NAMES[c]: int(round(lm[c], -1)) for c in gain + lose}
    R.d["r6_county_jobs"] = {W.NAMES[c]: GD.r10(G["total"][c]) for c in W.CODES}
    R.d["r7_changes"] = {W.NAMES[c]: GD.r1(ch[c]) for c in W.CODES}
    R.d["r8_designated"] = [W.NAMES[c] for c in des]
    R.d["r9_replay"] = dict(state_difference=round(rp["state_diff"], 2), mean_county_difference=round(rp["mean_abs"], 2))
    R.d["careful"] = dict(designated=[W.NAMES[c] for c in careful["designated"]],
                          changes={W.NAMES[c]: GD.r1(careful["change"][c]) for c in W.CODES})
    R.d["bands"] = dict(county_jobs={W.NAMES[c]: list(B["total"][c]) for c in W.CODES},
                        estimated={W.NAMES[c]: list(B["estimated"][c]) for c in W.CODES},
                        change={W.NAMES[c]: list(B["change"][c]) for c in W.CODES},
                        **{k_: list(v) for k_, v in B.items() if not isinstance(v, dict)},
                        latest_minus_site={W.NAMES[c]: list(B["latest_minus_site"][c]) for c in W.CODES})
    R.d["constants"] = dict(threshold=2.0, cutoff="15 February 2027", replay_cutoff="15 February 2026",
                            published_cut="31 May 2026", batch_min=3, arrived_share=0.5)
    R.d["routes"] = [dict(key=k_, name=x["name"], designated=[W.NAMES[c] for c in x["designated"]],
                          state_change=GD.r1(x["state_change"]), changes={W.NAMES[c]: GD.r1(x["change"][c]) for c in W.CODES})
                     for k_, x in zip(M.SHORTCUT_KEYS, G["routes"])]

    def rng(lo, hi, fmt="{:,}"):
        return "%s to %s" % (fmt.format(lo), fmt.format(hi))

    gap = min(abs(GD.r1(ch[c]) - W.THRESHOLD) for c in W.CODES if c not in des)
    # ---- Final Recommendation
    rec = ("Certify %s for the 2027 Community Transition Fund: on the records of 15 February 2027 their December 2026 covered "
           "jobs are an estimated %s per cent below December 2025, no other county is within %s of a point of the 2.0 per "
           "cent line (%s, the nearest, is at %s) and the state is at %s per cent. This rejects the estimate that carries "
           "every outstanding report alike, at the reporting employers' change times the share of such employers that "
           "reported in the end at earlier fourth-quarter cut-offs, and splits multi-county employers by their latest "
           "worksite report: it designates %s, with Garrow at %s and Kittredge at %s."
           % (names(des), ", ".join(f("chg_" + c, -GD.r1(ch[c]), pc1) for c in des[:-1]) + " and " + f("chg_" + des[-1], -GD.r1(ch[des[-1]]), pc1),
              f("margin_nearest", round(gap - 0.1, 1), pc1), W.NAMES[near], f("chg_near", GD.r1(ch[near]), pc1),
              f("state_change", GD.r1(G["state_change"]), "{:+.1f}"), names(careful["designated"]),
              f("careful_garrow", GD.r1(careful["change"]["009"]), pc1), f("careful_kittredge", GD.r1(careful["change"]["013"]), pc1)))

    # ---- Supplementary Questions
    S = []
    S.append("### ctf_certification_december_2026.xlsx\n")
    S.append("1. Sheet Certification names the counties to designate (%s) above a table with one row per county in "
             "county-code order: county code, county, December 2025 jobs as now on file, December 2026 jobs on reports "
             "received, December 2026 jobs estimated, December 2026 jobs, change on December 2025 (per cent) and designate, "
             "with a state row; county jobs to the nearest ten, the state's to the nearest hundred. Any figure inside the "
             "range shown beside it below is acceptable." % names(des))
    S.append("2. December 2026 jobs: " + "; ".join(
        "%s %s (%s)" % (W.NAMES[c], f("tot_" + c, GD.r10(G["total"][c])), rng(*map(int, B["total"][c]))) for c in W.CODES)
        + "; state %s (%s)." % (f("tot_state", GD.r100(G["state_total"])), rng(*map(int, B["state_total"]))))
    S.append("3. Of those, estimated (not on a report received by 15 February 2027): " + "; ".join(
        "%s %s (%s)" % (W.NAMES[c], f("est_" + c, GD.r10(G["estimated"][c])), rng(*map(int, B["estimated"][c]))) for c in W.CODES)
        + "; state %s (%s)." % (f("est_state", GD.r100(G["estimated"].sum())), rng(*map(int, B["state_estimated"]))))
    S.append("4. Change on December 2025, per cent: " + "; ".join(
        "%s %s (%s)" % (W.NAMES[c], f("chgs_" + c, GD.r1(ch[c]), pc1), rng(B["change"][c][0], B["change"][c][1], pc1)) for c in W.CODES)
        + "; state %s (%s)." % (f("chg_state", GD.r1(G["state_change"]), pc1), rng(B["state_change"][0], B["state_change"][1], pc1)))
    S.append("5. The chart is a column chart of the counties' changes with the minus 2.0 per cent line drawn across it; "
             "%s are the only columns at or below the line." % names(des))
    S.append("6. Sheet December 2025: the published fourth-quarter 2025 table counts %s December jobs and the records now "
             "hold %s, %s more: %s on reports received after 31 May 2026 from accounts established by then (%s accounts), "
             "%s on the reports of accounts established after 31 May 2026 (%s accounts) and %s net from reports amended "
             "after that day (%s reports); nothing is left unexplained."
             % (f("published", rc["published"]), f("now", rc["now"]), f("recon_diff", rc["now"] - rc["published"]),
                f("late_jobs", rc["late_jobs"]), f("late_n", rc["late_n"]), f("new_jobs", rc["new_jobs"]), f("new_n", rc["new_n"]),
                f("amend_jobs", rc["amend_jobs"]), f("amend_n", rc["amend_n"])) +
             " December 2025 as now on file is the reports on file: the %s employers liable for that quarter that have still "
             "filed no report for it, silent for five quarters, are counted at nought (carried at their last report they "
             "would add about %s jobs, which the ranges on the changes allow for)."
             % (f("base_silent_n", G["base_silent"]["n"]), f("base_silent_jobs", int(round(G["base_silent"]["jobs"], -1)))))
    S.append("7. Sheet Replay December 2025: the same estimate made for December 2025 from the records as they stood on 15 "
             "February 2026 gives %s jobs for the state against %s now on file, a difference of %s per cent (%s "
             "acceptable), and differs from the figures now on file by %s per cent for the average county (%s "
             "acceptable); every share and count in it is measured on what was on file that day, and the ranges allow for "
             "a sound estimate whose count of unregistered employers ran lower a year earlier."
             % (f("replay_state", GD.r100(rp["state_total"])), f("base_state", GD.r100(G["base"].sum())),
                f("replay_diff", round(rp["state_diff"], 2), pc2), rng(B["replay_state_diff"][0], B["replay_state_diff"][1], pc2),
                f("replay_mean_abs", round(rp["mean_abs"], 2), pc2),
                rng(B["replay_mean_abs"][0], B["replay_mean_abs"][1], pc2) if B["replay_mean_abs"][0] > 0
                else "up to " + pc2.format(B["replay_mean_abs"][1])))
    S.append("\n### ctf_employer_jobs_december_2026.csv\n")
    S.append("8. One row for each liable employer with an account and each county in which it has a worksite, then one row "
             "per county for the employers with no account yet, %s rows in all, with columns account_no, legal_name, "
             "county_code, county, report_received (Y or N), december_2026_jobs (to one decimal) and basis. The %s liable "
             "accounts are %s with a report received and %s without. The basis column is this file's own reading of why "
             "each of the %s is outstanding, under conventions it states (a payroll agent's batch is three or more reports "
             "received in the same second; a batch has arrived when half of its other employers have reported; every "
             "quarter means every report of the last four came after its cut-off), and another sound convention moves the "
             "counts inside the ranges given: %s (%s) whose usual batch had not arrived; %s (%s) outstanding on their own, "
             "their usual batch having arrived without them or the employer filing singly; %s (%s) that file after the "
             "cut-off every quarter (the last two are %s together, %s); %s (%s) with no report for two quarters; and %s "
             "(%s) new accounts whose first report had not arrived."
             % (f("csv_rows", G["n_rows"]), f("liable", cz["liable"]), f("received", cz["received"]), f("outstanding", cz["outstanding"]),
                f("outstanding_b", cz["outstanding"]),
                f("n_batch", G["kinds"]["batch"]["n"]), rng(*B["n_batch"]), f("n_alone", G["kinds"]["alone"]["n"]), rng(*B["n_alone"]),
                f("n_habit", G["kinds"]["habit"]["n"]), rng(*B["n_habit"]),
                f("n_alone_habit", G["kinds"]["alone"]["n"] + G["kinds"]["habit"]["n"]), rng(*B["n_alone_habit"]),
                f("n_twoq", G["kinds"]["twoq"]["n"]), rng(*B["n_twoq"]), f("n_new", G["kinds"]["new"]["n"]), rng(*B["n_new"])))
    S.append("\n### ctf_certification_memo_2027.docx\n")
    S.append("9. One page to the Commissioner of Labor: the counties to designate (%s) first with their December jobs and "
             "changes, then what the estimates rest on: the outstanding reports read by cause, those outstanding on their "
             "own carried at %s of their September jobs; why this quarter cannot be carried at the closed quarters' pooled "
             "experience (employers outstanding on their own hold %s per cent of construction employers' September jobs, "
             "%s acceptable, against %s per cent a year earlier and under one per cent at every earlier fourth-quarter "
             "cut-off); about %s employers with no account yet and their %s jobs; each worksite carried by its own "
             "December-on-September change a year earlier; and how far the same estimate was out for December 2025."
             % (names(des), f("k_alone", round(G["k_alone"], 2), pc2), f("trouble_now", round(100 * tr[15]["constr"], 1), pc1),
                rng(B["trouble_constr"][0], B["trouble_constr"][1], pc1), f("trouble_2025", round(100 * tr[11]["constr"], 1), pc1),
                f("unreg_n", int(round(ui["n"], -1))), f("unreg_jobs", GD.r100(G["unreg_jobs"]))))

    # ---- Critical Components: three results every sound estimate has to compute, from three areas of the chain
    C = []
    C.append("1. Of the **%s** reports outstanding, **%s** (%s acceptable) belong to employers whose usual batch (three or "
             "more reports received in the same second) had not arrived and **%s** (%s) are outstanding on their own or "
             "late every quarter; on the quarters %s to %s, whose outstanding employers have all since resolved, an employer "
             "outstanding on its own kept **%s** of its September jobs (%s acceptable) and one in a late batch %s, so the "
             "two cannot be carried alike."
             % (f("outstanding2", cz["outstanding"]), f("n_batch2", G["kinds"]["batch"]["n"]), rng(*B["n_batch"]),
                f("n_alone_habit2", G["kinds"]["alone"]["n"] + G["kinds"]["habit"]["n"]), rng(*B["n_alone_habit"]),
                W.quarter_label(G["mature"][0]), W.quarter_label(G["mature"][-1]), f("k_alone2", round(G["k_alone"], 2), pc2),
                rng(B["k_alone"][0], B["k_alone"][1], pc2), f("k_batch_hist", round(G["k_batch_hist"], 2), pc2)))
    C.append("2. The fourth-quarter worksite report of %s of the %s multi-county employers was still out; carrying each of "
             "their worksites by its own December-on-September change a year earlier puts about %s than the latest "
             "worksite reports' split, and about %s."
             % (f("sites_carried", st["carried"]), f("sites_multi", st["multi"]),
                listed(["**%s** fewer %sin %s (%s)" % (f("lm_" + c, int(round(lm[c], -1))), "December jobs " if i == 0 else "",
                                                       W.NAMES[c], rng(*map(int, B["latest_minus_site"][c]))) for i, c in enumerate(gain)]),
                listed(["%s more in %s" % (f("lm_" + c, -int(round(lm[c], -1))), W.NAMES[c]) for c in lose])))
    C.append("3. About **%s** employers liable for the quarter had no account at the cut-off (%s acceptable), with about "
             "**%s** December jobs (%s): %s new employers of the quarter had an account by then, %s more were set up later "
             "for each one registered at earlier fourth-quarter cut-offs, and the late ones had %s jobs each. Last year's "
             "unregistered jobs carried as they were give %s."
             % (f("unreg_n2", int(round(ui["n"], -1))), rng(*map(int, B["unreg_n"])), f("unreg_jobs2", GD.r100(G["unreg_jobs"])),
                rng(*map(int, B["unreg_jobs"])), f("reg_own", ui["reg_own"]), f("c_own", round(ui["c_own"], 1), pc1),
                f("j_own", round(ui["j_own"], 1), pc1), f("unreg_level", GD.r100(level["unreg_jobs"]))))

    # ---- Step-by-Step
    T = []
    T.append("1. Conformed the Division's four extracts as they stood at the close of 15 February 2027: the latest version "
             "of each report in ui_quarterly_reports_2023q1_2026q4.csv (a resubmission once; a report counts once its "
             "account is established), the accounts liable for the fourth quarter of 2026 from "
             "ui_employer_accounts_2027-02-15.csv and ui_account_status_history_2023-2027.csv (established by the "
             "cut-off, liable by 31 December, not closed, inactivated or transferred with effect by 1 October), and "
             "ui_multiple_worksite_reports_2023q1_2026q4.csv for worksite counties: %s liable accounts, %s reports "
             "received, %s outstanding."
             % (f("liable3", cz["liable"]), f("received3", cz["received"]), f("outstanding3", cz["outstanding"])))
    T.append("2. December 2025 from every fourth-quarter 2025 report now on file, split by worksite: %s jobs, %s above the "
             "%s in covered_employment_by_county_2025q4.xlsx, which counts reports posted through 31 May 2026 (late "
             "reports %s, accounts established since %s, amendments %s)."
             % (f("now3", rc["now"]), f("recon_diff3", rc["now"] - rc["published"]), f("published3", rc["published"]),
                f("late_jobs3", rc["late_jobs"]), f("new_jobs3", rc["new_jobs"]), f("amend_jobs3", rc["amend_jobs"])))
    T.append("3. Read each outstanding report by why it is outstanding. Rebuilt the payroll agents' batches from received_at "
             "(three or more reports in the same second) and asked whether the batch an employer's third-quarter report "
             "came in had arrived (at least half of its other employers reported): %s in batches not yet received, %s "
             "outstanding on their own, %s late every quarter, %s with no third-quarter report, %s new accounts. The "
             "hurried reading carries them all alike: at the reporting employers' change times the %s of such employers "
             "that reported in the end at earlier fourth-quarter cut-offs it designates %s, and at the reporting "
             "employers' change alone %s."
             % (f("n_batch3", G["kinds"]["batch"]["n"]), f("n_alone3", G["kinds"]["alone"]["n"]), f("n_habit3", G["kinds"]["habit"]["n"]),
                f("n_twoq3", G["kinds"]["twoq"]["n"]), f("n_new3", G["kinds"]["new"]["n"]),
                f("pooled_survive", round(G["pooled"]["survive"], 2), pc2), names(surv["designated"]), names(rep_all["designated"])))
    T.append("4. Measured what such employers turned out to have at the cut-offs of %s to %s, every one since resolved by a "
             "late report, a closure or an inactivation: outstanding on their own kept %s of September, in a late batch "
             "%s, two quarters out %s. Every closed quarter reads %s with the unresolved left out (the latest quarters' "
             "closures are not yet recorded) and %s with them at nought; the range on the share takes in both."
             % (W.quarter_label(G["mature"][0]), W.quarter_label(G["mature"][-1]), f("k_alone3", round(G["k_alone"], 2), pc2),
                f("k_batch_hist3", round(G["k_batch_hist"], 2), pc2), f("k_twoq", round(G["k_twoq"], 3), "{:.3f}"),
                f("k_allclosed", round(G["k_allclosed"], 2), pc2), f("k_allzero", round(G["k_allzero"], 2), pc2)))
    T.append("5. Set this quarter against the closed ones before carrying anything over from them: employers outstanding "
             "on their own number %s against %s a year earlier and hold %s per cent of construction employers' September "
             "jobs against %s, %s and %s per cent at the fourth-quarter cut-offs of 2023, 2024 and 2025, so a share or a "
             "survival rate pooled over every outstanding report at earlier cut-offs does not describe this quarter's. "
             "Carried the employers in late batches (and the habitually late) at the reporting employers' "
             "December-on-September change in their county and supersector, except for this quarter's share of jobs at "
             "employers outstanding on their own, by supersector and size, which is carried at %s: about %s fewer jobs "
             "than the reporters' change alone, construction employers at %s of September against %s. An estimate without "
             "this last refinement stays inside every range above; the replay cannot test it, December 2025 having had no "
             "such quarter."
             % (f("n_alone4", tr[15]["n_alone"]), f("n_alone_2025b", tr[11]["n_alone"]),
                f("trouble_now2", round(100 * tr[15]["constr"], 1), pc1), f("trouble_2023", round(100 * tr[3]["constr"], 1), pc1),
                f("trouble_2024", round(100 * tr[7]["constr"], 1), pc1), f("trouble_2025b", round(100 * tr[11]["constr"], 1), pc1),
                f("k_alone4", round(G["k_alone"], 2), pc2), f("transport_jobs", int(round(G["transport_jobs"], -1))),
                f("kept_constr", round(G["kept_constr"], 2), pc2), f("kept_constr_reporters", round(G["reporters"]["kept_constr"], 2), pc2)))
    dB = [abs(noB["change"][c] - ch[c]) for c in W.CODES]
    T.append("6. Added the employers liable for the quarter with no account yet: %s new employers of the quarter were "
             "registered by the cut-off; at the fourth-quarter cut-offs of 2023 to 2025, %s accounts were established "
             "later for each one registered by then, with %s December jobs each; with the stragglers of earlier quarters, "
             "about %s employers and %s jobs, county by county. Left out, every county reads %s to %s of a point lower and "
             "the state reads %s per cent instead of %s."
             % (f("reg_own3", ui["reg_own"]), f("c_own3", round(ui["c_own"], 1), pc1), f("j_own3", round(ui["j_own"], 1), pc1),
                f("unreg_n3", int(round(ui["n"], -1))), f("unreg_jobs3", GD.r100(G["unreg_jobs"])),
                f("noB_min", round(GD.down(min(dB), 0.1), 1), pc1), f("noB_max", round(GD.up(max(dB), 0.1), 1), pc1),
                f("noB_state", GD.r1(noB["state_change"]), pc1), f("state_change3", GD.r1(G["state_change"]), "{:+.1f}")))
    T.append("7. Split each multi-county employer by its fourth-quarter worksite report where it was on file (%s of %s) and "
             "otherwise by its latest report with each worksite carried by its own change between the same two quarters a "
             "year earlier. The latest reports' split as it stands puts Kittredge at %s per cent and Talcott at %s."
             % (f("sites_own", st["own"]), f("sites_multi3", st["multi"]), f("latest_kit", GD.r1(latest["change"]["013"]), pc1),
                f("latest_tal", GD.r1(latest["change"]["023"]), pc1)))
    T.append("8. Summed by worksite county and set against the December before: %s; %s next at %s; designated %s."
             % ("; ".join("%s %s" % (W.NAMES[c], f("chg3_" + c, GD.r1(ch[c]), pc1)) for c in des), W.NAMES[near],
                f("chg_near3", GD.r1(ch[near]), pc1), names(des)))
    T.append("9. Replayed the whole estimate for December 2025 from the records as they stood on 15 February 2026 (resolved "
             "quarters %s to %s, every count as it stood that day): %s per cent from the state figure now on file, %s per "
             "cent for the average county."
             % (W.quarter_label(rp["mature"][0]), W.quarter_label(rp["mature"][-1]), f("replay_diff3", round(rp["state_diff"], 2), pc2),
                f("replay_mean_abs3", round(rp["mean_abs"], 2), pc2)))
    close = ("No other set survives. Carrying every outstanding report alike designates %s (with the share that reported in "
             "the end at earlier cut-offs) or %s (at the reporting employers' change, or at what such reports kept at "
             "earlier fourth-quarter cut-offs) and puts Garrow at %s to %s; it is refuted by the resolved quarters, where "
             "employers outstanding on their own kept %s of their September jobs against %s in late batches, and by this "
             "quarter's %s such employers against %s a year earlier. Counting only employers with an account designates %s "
             "but puts every county %s to %s of a point too low, and section 5(b) counts employers whether or not an "
             "account has been established. The latest worksite reports' split designates %s and puts Kittredge at %s, "
             "because it places the lake worksites' summer jobs there in December; the worksite reports of earlier years "
             "show the same worksites falling every December. Every reading inside the estimate (a batch as two, three or "
             "four reports in one second; arrived at a third, a half or two thirds of its other employers; this quarter's "
             "share carried to the late batches or not, by supersector, three-digit industry or a hand-picked group of "
             "housing industries, with or without size; the resolved quarters with the earliest or the latest left out, or "
             "every closed quarter; the share kept by size, channel or industry group; late every quarter as all or three "
             "of the last four reports, and the habitually late carried with the late batches or at the reporters' change; "
             "a late employer by its county and supersector or by its own change a year earlier; unregistered employers "
             "developed on fourth-quarter cut-offs or on every cut-off; a worksite by its own change a year earlier or by "
             "last December's split; the employers still silent for December 2025 at nought or at their last report) "
             "designates the same three counties with every figure inside the ranges above."
             % (names(surv["designated"]), names(rep_all["designated"]),
                f("pooled_garrow_lo", min(GD.r1(x["change"]["009"]) for x in (surv, kept, rep_all)), pc1),
                f("pooled_garrow_hi", max(GD.r1(x["change"]["009"]) for x in (surv, kept, rep_all)), pc1),
                f("k_alone5", round(G["k_alone"], 2), pc2), f("k_batch_hist5", round(G["k_batch_hist"], 2), pc2),
                f("n_alone5", tr[15]["n_alone"]), f("n_alone_2025", tr[11]["n_alone"]), names(noB["designated"]),
                f("noB_min2", round(GD.down(min(dB), 0.1), 1), pc1), f("noB_max2", round(GD.up(max(dB), 0.1), 1), pc1),
                names(latest["designated"]), f("latest_kit2", GD.r1(latest["change"]["013"]), pc1)))
    md = ("## Tags\n\n**Domain:** Other, Survey Research & Official Statistics (census, register and administrative-data quality).  \n"
          "**Analysis type:** Data Extraction & Conformation (ETL / Pipeline Build).\n\n"
          "## Final Recommendation\n\n" + rec + "\n\n## Supplementary Questions\n\n" + "\n".join(S) +
          "\n\n## Critical Components\n\n" + "\n".join(C) + "\n\n## Step-by-Step\n\n" + "\n".join(T) + "\n\n" + close + "\n")
    return R.d, md


def write(task, w, T, pk, G, n):
    figs, md = figures_and_blocks(pk, G, n)
    figs["rows"] = {k: int(v) for k, v in n.items()}
    json.dump(figs, open(os.path.join(task, "generator", "figures.json"), "w"), indent=1, ensure_ascii=False, sort_keys=True)
    open(os.path.join(task, "submission.md"), "w", encoding="utf-8").write(md)
    return figs
